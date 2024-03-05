import argparse
import json
import os
import re

from . import Validator
from .constants import CheckResult, TestFile
from .parser import check_event_category_to_type_mapping


class TestFileValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        format_path = result.options["path"]

        test_folder = os.path.join(format_path, "tests")
        if not os.path.exists(test_folder):
            if not args.ignore_missing_tests:
                result.errors.append("tests folder does not exist")
            return

        test_paths = find_tests(test_folder)
        if len(test_paths) == 0:
            if not args.ignore_missing_tests:
                result.errors.append("no test found")
            return

        for test_path in test_paths:
            check_test_file(
                test_path=test_path,
                ignore_event_fieldset_errors=args.ignore_event_fieldset_errors,
                result=result,
            )


def find_tests(tests_path: str) -> list[str]:
    result: list[str] = []

    for element in os.listdir(tests_path):
        if element.endswith(".json"):
            result.append(os.path.join(tests_path, element))

    return result


def check_test_file(
    test_path: str, ignore_event_fieldset_errors: bool, result: CheckResult
) -> None:
    try:
        with open(test_path, "rt") as file:
            test_content = json.load(file)

        test_parsed = TestFile.model_validate(test_content)

        test_time_stamp = test_parsed.expected.get("@timestamp")
        re_rfc3339 = re.compile(
            r"^((?:(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})?)$"
        )

        if test_time_stamp and not re.match(re_rfc3339, test_time_stamp):
            result.errors.append(f"Incorrect @timestamp in the test {test_path}")

        if "event" in test_parsed.expected and not ignore_event_fieldset_errors:
            event = test_parsed.expected["event"]

            event_type_readable = False
            event_category_readable = False

            if "type" in event:
                if type(event["type"]) != list:
                    result.errors.append(
                        f"event.type is not a list in a test {test_path}"
                    )
                else:
                    event_type_readable = True

            if "category" in event:
                if type(event["category"]) != list:
                    result.errors.append(
                        f"event.category is not a list in test {test_path}"
                    )
                else:
                    event_category_readable = True

            if event_type_readable and event_category_readable:
                check_mapping = check_event_category_to_type_mapping(
                    event_categories=event["category"], event_types=event["type"]
                )
                if not check_mapping:
                    result.errors.append(
                        f"`event.type` does not match the type associated to the `event.category` in {test_path}"
                    )

        elif not ignore_event_fieldset_errors:
            result.errors.append(
                f"No event.category and event.type declared as `expected` in {test_path}"
            )

    except Exception as any_error:
        result.errors.append(
            f"test {test_path} exists, but cannot be loaded (`{any_error}`)"
        )
