import glob
import json
import os
import subprocess
from collections import defaultdict
from typing import Tuple

import pytest
import requests
import yaml

VALIDATION_URL = "https://app.sekoia.io/api/v1/ingest/formats/validate"
INTAKES_PATH = os.path.dirname(os.path.dirname(__file__))


class FormatError(Exception):
    pass


class IntakeTestManager:
    def __init__(self):
        self._intakes = {}
        self._results = defaultdict(dict)

    def load(self, modules: list[str], intake_formats: list[str]):
        """Load the hierarchy of modules, parsers and tests"""
        filtered_elements = {".git", ".github", "doc", "utils"}

        for subdir in os.listdir(INTAKES_PATH):
            if subdir not in filtered_elements and (not modules or subdir in modules):
                module_path = os.path.join(INTAKES_PATH, subdir)
                if os.path.isdir(module_path):
                    self._intakes[subdir] = self._get_formats(module_path, intake_formats)

    def _get_formats(self, module_path: str, intake_formats: list[str]) -> dict[str, list[str]]:
        formats = {}

        filtered_elements = {"_meta"}

        for subdir in os.listdir(module_path):
            if subdir not in filtered_elements and (not intake_formats or subdir in intake_formats):
                format_path = os.path.join(module_path, subdir)
                if os.path.isdir(format_path) and os.path.isfile(os.path.join(format_path, "ingest", "parser.yml")):
                    formats[subdir] = self._get_tests(format_path)

        return formats

    def _get_tests(self, format_path: str) -> list[str]:
        tests = []

        for test_file in glob.glob(f"{format_path}/tests/*.json"):
            tests.append(os.path.relpath(test_file, INTAKES_PATH))

        return tests

    def testcases(self) -> list[str]:
        results = []

        for _, module in self._intakes.items():
            for _, tests in module.items():
                results += tests

        return results

    def formats(self) -> list[Tuple[str, str]]:
        results = []

        for module, module_dict in self._intakes.items():
            for intake_format in module_dict:
                results.append((module, intake_format))

        return results

    def _get_format_results(self, module: str, intake_format: str) -> dict:
        if module not in self._results or intake_format not in self._results[module]:
            module_path = os.path.join(INTAKES_PATH, module)
            format_path = os.path.join(module_path, intake_format)

            with open(os.path.join(format_path, "ingest", "parser.yml")) as f:
                parser = yaml.safe_load(f)

            fields = {}
            module_fields_path = os.path.join(module_path, "_meta", "fields.yml")
            format_fields_path = os.path.join(format_path, "_meta", "fields.yml")

            for fields_path in [module_fields_path, format_fields_path]:
                if os.path.isfile(fields_path):
                    with open(fields_path) as f:
                        content = yaml.safe_load(f)
                        if content and isinstance(content, dict):
                            fields.update(content)

            messages = []
            for test in self._intakes[module][intake_format]:
                with open(os.path.join(INTAKES_PATH, test)) as f:
                    message = json.load(f)
                    messages.append(message["input"]["message"])

            response = requests.post(
                VALIDATION_URL,
                json={
                    "parser": parser,
                    "taxonomy": list(fields.values()),
                    "messages": messages,
                },
            )
            if not response.ok:
                raise FormatError(f"{response.status_code} {response.reason} for {response.url}: {response.content} ")
            response.raise_for_status()
            self._results[module][intake_format] = response.json()
            self._results[module][intake_format]["parsed_messages"] = {
                test: self._results[module][intake_format]["parsed_messages"][i]
                for i, test in enumerate(self._intakes[module][intake_format])
            }

        return self._results[module][intake_format]

    def get_parsed_message(self, test_path: str) -> dict:
        parts = test_path.split("/")
        results = self._get_format_results(parts[0], parts[1])
        return results["parsed_messages"].get(test_path, {})

    def get_coverage(self, module: str, intake_format: str) -> dict:
        results = self._get_format_results(module, intake_format)
        return results["coverage"]

    def get_taxonomy(self, module: str, intake_format: str) -> dict:
        results = self._get_format_results(module, intake_format)
        return results["taxonomy"]


_manager = IntakeTestManager()


def pytest_addoption(parser):
    parser.addoption(
        "--module",
        action="append",
        default=[],
        help="name of the module to test",
    )

    parser.addoption(
        "--format",
        action="append",
        default=[],
        help="name of the format to test",
    )

    parser.addoption(
        "--changes",
        action="store_true",
        default=False,
        help="only check formats that were modified",
    )

    parser.addoption(
        "--fix-expectations",
        action="store_true",
        default=False,
        help="update test files to replace expected with the actual result",
    )

    parser.addoption(
        "--prune-taxonomy",
        action="store_true",
        default=False,
        help="Remove unused fields from fields.yml (aka taxonomy)",
    )

    parser.addoption(
        "--fix-missing-fields",
        action="store_true",
        default=False,
        help="Add missing fields into fields.yml (aka taxonomy)",
    )


def pytest_configure(config):
    modules = config.getoption("module")
    intake_formats = config.getoption("format")

    if config.getoption("changes"):
        check_all = False
        changed_modules = set()
        changed_formats = set()

        result = subprocess.run(["git", "diff", "--name-only", "origin/main"], capture_output=True)
        for changed_file in result.stdout.splitlines():
            changed_file = changed_file.decode()
            parts = changed_file.split("/")

            if parts[-1] in ["conftest.py", "test_formats.py"]:
                check_all = True
                break

            if len(parts) > 2:
                changed_modules.add(parts[0])
                changed_formats.add(parts[1])

        if check_all:
            modules = []
            intake_formats = []
        else:
            modules = list(changed_modules)
            intake_formats = list(changed_formats)

    _manager.load(modules=modules, intake_formats=intake_formats)


def pytest_generate_tests(metafunc):
    if "test_path" in metafunc.fixturenames:
        metafunc.parametrize("test_path", _manager.testcases())
    elif "intake_format" in metafunc.fixturenames:
        metafunc.parametrize("module,intake_format", _manager.formats())


@pytest.fixture
def manager():
    return _manager


@pytest.fixture
def intakes_root():
    return INTAKES_PATH


@pytest.fixture
def module(config):
    return config.getoption("module")


@pytest.fixture
def module_path(intakes_root, module):
    return os.path.join(INTAKES_PATH, module)


@pytest.fixture
def format_path(module_path, intake_format):
    return os.path.join(module_path, intake_format)


@pytest.fixture
def module_fields_path(module_path):
    return os.path.join(module_path, "_meta", "fields.yml")


@pytest.fixture
def format_fields_path(format_path):
    return os.path.join(format_path, "_meta", "fields.yml")
