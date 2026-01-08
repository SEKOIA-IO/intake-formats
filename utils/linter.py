import argparse
import difflib
import json
import subprocess
from pathlib import Path

import yaml

from conftest import IntakeTestManager
from helpers import YamlDumper, format_test

INTAKES_PATH = Path(__file__).parent.parent


def find_changed_modules_and_formats() -> (list, list):
    diff = subprocess.run(["git", "diff", "--name-only", "origin/main"], capture_output=True)

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
    short_path = str(taxonomy_path).replace(str(INTAKES_PATH), "")

    if input_yaml != expected_yaml:
        if not fix:
            need_fix = True
            print(f"{short_path} should be fixed:")
            print(get_diff_between(input_yaml, expected_yaml))

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
    short_path = str(test_path).replace(str(INTAKES_PATH), "")

    if current_test != expected_test:
        if not fix:
            need_fix = True
            print(f"{short_path} should be fixed:")
            print(get_diff_between(current_test, expected_test))
            print()

        else:
            with open(test_path, "wt") as file:
                file.write(expected_test)

            print(f"{short_path} fixed")

    return need_fix


def check_parser(parser_path: Path | str) -> bool:
    """
    Check parser for redundancies, such as empty descriptions and filters
    """
    need_fixes = False
    if not parser_path.is_file():
        return False

    with open(parser_path, "rt") as file:
        raw = yaml.safe_load(file)

    # check pipeline steps
    for step in raw["pipeline"]:
        step_name = step["name"]
        if "filter" in step and (step["filter"] is None or len(step["filter"]) == 0):
            need_fixes = True
            print(f"{parser_path} needs to be fixed: remove empty filter at `{step_name}` step in pipeline")

        if "description" in step and (step["description"] is None or len(step["description"]) == 0):
            need_fixes = True
            print(f"{parser_path} needs to be fixed: remove empty description at `{step_name}` step in pipeline")

    # check stages
    for stage_name, stage in raw["stages"].items():
        for action in stage["actions"]:
            if "set" in action and action.get("name") == "set":
                need_fixes = True
                print(f"{parser_path} needs to be fixed: remove `name: set` from `{stage_name}` stage")

    return need_fixes


def get_diff_between(t1: str, t2: str) -> str:
    green = "\x1b[38;5;16;48;5;2m"
    red = "\x1b[38;5;16;48;5;1m"
    end = "\x1b[0m"

    differ = difflib.Differ()
    lines_1 = t1.split("\n")
    lines_2 = t2.split("\n")

    diff = differ.compare(lines_1, lines_2)

    # add some color
    result_lines = []
    for line in diff:
        if line.startswith("+"):
            result_lines.append(green + line + end)

        elif line.startswith("-"):
            result_lines.append(red + line + end)

        else:
            result_lines.append(line)

    return "\n".join(result_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linter")
    parser.add_argument("action", choices=["check", "fix"])
    parser.add_argument("--format", action="append", default=[], help="Check/Fix specific formats")
    parser.add_argument("--module", action="append", default=[], help="Check/Fix specific modules")
    parser.add_argument("--changes", action="store_true", help="Check/Fix only changed files")
    args = parser.parse_args()

    if args.changes:
        modules, formats = find_changed_modules_and_formats()

    else:
        modules, formats = args.module, args.format

    mngr = IntakeTestManager()
    mngr.load(modules=modules, intake_formats=formats)

    # Check whether we found all requested modules/formats
    found_formats = mngr.formats()
    if args.changes and len(found_formats) == 0:
        print("No changes detected")
        exit()

    all_found_modules = set(item[0] for item in found_formats)
    all_found_formats = set(item[1] for item in found_formats)
    missed_modules = set(args.module) - all_found_modules
    missed_formats = set(args.format) - all_found_formats
    if len(missed_modules) > 0 or len(missed_formats) > 0:
        if len(missed_modules) > 0:
            print(f"Module(s) `{','.join(missed_modules)}` not found")

        if len(missed_formats) > 0:
            print(f"Format(s) `{','.join(missed_formats)}` not found")

        exit(1)

    # Collect taxonomies and parsers to check
    taxonomies = set()
    parsers = set()

    for (
        module_name,
        format_name,
    ) in mngr.formats():
        module_path = INTAKES_PATH / module_name
        format_path = module_path / format_name

        module_taxonomy = module_path / "_meta" / "fields.yml"
        if module_taxonomy.exists():
            taxonomies.add(module_taxonomy)

        format_taxonomy = format_path / "_meta" / "fields.yml"
        if format_taxonomy.exists():
            taxonomies.add(format_taxonomy)

        format_parser = format_path / "ingest" / "parser.yml"
        if format_parser.exists():
            parsers.add(format_parser)

    taxonomies = sorted(list(taxonomies))

    need_fix = False
    expect_fix = args.action == "fix"

    for path in taxonomies:
        need_fix |= check_taxonomy(INTAKES_PATH / path, fix=expect_fix)

    # Collect tests to test
    for path in mngr.testcases():
        need_fix |= check_test_file(INTAKES_PATH / path, fix=expect_fix)

    need_manual_fix = False
    for path in parsers:
        result = check_parser(INTAKES_PATH / path)
        need_fix |= result
        need_manual_fix |= result

    if need_fix and not need_manual_fix:
        print()
        print("To fix, use `python utils/linter.py fix --changes`")
        exit(1)

    elif need_manual_fix:
        print()
        print("You have to fix these errors manually")
        exit(1)

    else:
        print("Everything looks ok")
