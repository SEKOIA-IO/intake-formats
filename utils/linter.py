import json
import subprocess

import yaml
import argparse
from pathlib import Path
from helpers import YamlDumper, format_test
from conftest import IntakeTestManager

INTAKES_PATH = Path(__file__).parent.parent


def find_changed_modules_and_formats() -> (list, list):
    diff = subprocess.run(
        ["git", "diff", "--name-only", "origin/main"], capture_output=True
    )

    changed_modules = set()
    changed_formats = set()

    for changed_file in diff.stdout.splitlines():
        # always path from the root of git repo
        changed_file = changed_file.decode()
        parts = changed_file.split("/")

        if len(parts) > 2:
            changed_modules.add(parts[0])
            changed_formats.add(parts[1])

    return list(changed_modules), list(changed_formats)


def check_taxonomy(taxonomy_path: str | Path, fix: bool = False) -> bool:
    need_fix = False

    with open(taxonomy_path, "rt") as file:
        input_yaml = file.read()

    fields = yaml.safe_load(input_yaml)
    if not fields:
        return False

    expected_yaml = yaml.dump(data=fields, Dumper=YamlDumper, sort_keys=True)
    short_path = str(taxonomy_path).lstrip(str(INTAKES_PATH))

    if input_yaml != expected_yaml:
        if not fix:
            need_fix = True
            print(f"{short_path} should be fixed")

        else:
            with open(taxonomy_path, "wt") as file:
                file.write(expected_yaml)

            print(f"{short_path} fixed")

    return need_fix


def check_test_file(test_path: str | Path, fix: bool = False) -> bool:
    need_fix = False

    with open(test_path, "rt") as file:
        current_test = file.read()
        current_test_json = json.loads(current_test)

    expected_test_json = format_test(current_test_json)
    expected_test = json.dumps(expected_test_json, indent=2)
    short_path = str(test_path).lstrip(str(INTAKES_PATH))

    if current_test != expected_test:
        if not fix:
            need_fix = True
            print(f"{short_path} should be fixed")

        else:
            with open(test_path, "wt") as file:
                file.write(expected_test)

            print(f"{short_path} fixed")

    return need_fix


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linter")
    parser.add_argument("action", choices=["check", "fix"])
    parser.add_argument(
        "--format", action="append", default=[], help="Check/Fix specific format"
    )
    parser.add_argument(
        "--module", action="append", default=[], help="Check/Fix specific module"
    )
    parser.add_argument(
        "--changes", action="store_true", help="Check/Fix only changed files"
    )
    args = parser.parse_args()

    if args.changes:
        modules, formats = find_changed_modules_and_formats()

    else:
        modules, formats = args.module, args.format

    mngr = IntakeTestManager()
    mngr.load(modules=modules, intake_formats=formats)

    # Collect taxonomies to check
    taxonomies = set()
    for (
        module_name,
        format_name,
    ) in mngr.formats():
        module_path = Path(module_name)
        format_path = module_path / format_name

        module_taxonomy = module_path / "_meta" / "fields.yml"
        if module_taxonomy.exists():
            taxonomies.add(module_taxonomy)

        format_taxonomy = format_path / "_meta" / "fields.yml"
        if format_taxonomy.exists():
            taxonomies.add(format_taxonomy)

    taxonomies = sorted(list(taxonomies))

    need_fix = False
    expect_fix = args.action == "fix"

    for path in taxonomies:
        need_fix |= check_taxonomy(INTAKES_PATH / path, fix=expect_fix)

    # Collect tests to test
    for path in mngr.testcases():
        need_fix |= check_test_file(INTAKES_PATH / path, fix=expect_fix)

    if need_fix:
        print()
        print("To fix, use `python utils/linter.py fix --changes`")
        exit(1)

    else:
        print("Everything looks ok")
