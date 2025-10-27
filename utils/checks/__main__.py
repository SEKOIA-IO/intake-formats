import argparse
import os
import subprocess
import sys
import json
from pathlib import Path

from validators.constants import CheckResult
from validators.format import FormatValidator
from validators.module import ModuleValidator

INTAKES_PATH = Path(__file__).parent.parent.parent


def find_modules(root_path: Path) -> list[Path]:
    """
    Return the path to all the potential modules
    """
    module_paths: list[Path] = []

    filtered_elements = {"doc", "utils"}

    for element_path in root_path.iterdir():
        if element_path.name not in filtered_elements and not element_path.name.startswith("."):
            if element_path.is_dir():
                module_paths.append(element_path)

    return sorted(module_paths)


def find_formats(root_path: Path, formats: list[Path] | None = None) -> list[Path]:
    """
    Return the path to all the potential formats
    """
    format_paths: list[Path] = list()

    filtered_elements = {"_meta"}

    for element_path in root_path.iterdir():
        if element_path.name not in filtered_elements:
            if element_path.is_dir():
                if formats:
                    if element_path.name not in formats:
                        continue

                format_paths.append(element_path)

    return sorted(format_paths)


def check_format(path: Path, module_result: CheckResult, args: argparse.Namespace) -> CheckResult:
    valid = FormatValidator(path=path, module_result=module_result, args=args)
    valid.validate()

    return valid.result


def check_module_formats(
    module_result: CheckResult, formats: list[str] | None, args: argparse.Namespace
) -> list[CheckResult]:
    module_formats = find_formats(module_result.options["path"], formats=formats)

    result = [
        check_format(path=module_format, module_result=module_result, args=args) for module_format in module_formats
    ]

    return result


def check_module_uuids_and_slugs(check_module_results: list[CheckResult]):
    # module uuids are unique
    module_uuids: dict[str, str] = dict()
    for module_result in check_module_results:
        if (
            len(module_result.errors) == 0
            and "manifest_uuid" in module_result.options
            and module_result.options["manifest_uuid"] in module_uuids
        ):
            module_result.errors.append(
                f"module have the same uuid ({module_result.options['manifest_uuid']}) "
                f"than module {module_uuids[module_result.options['manifest_uuid']]}"
            )

            module_uuids[module_result.options["manifest_uuid"]] = module_result.options.get(
                "manifest_uuid", "unknown"
            )

    # module slugs are unique
    module_slugs: dict[str, str] = dict()
    for module_result in check_module_results:
        if (
            len(module_result.errors) == 0
            and "manifest_slug" in module_result.options
            and module_result.options["manifest_slug"] in module_slugs
        ):
            module_result.errors.append(
                f"module have the same slug ({module_result.options['manifest_slug']}) "
                f"than module {module_slugs[module_result.options['manifest_slug']]}"
            )

            module_slugs[module_result.options["manifest_slug"]] = module_result.options.get(
                "manifest_slug", "unknown"
            )


def check_format_uuids_and_slugs(check_format_results: list[CheckResult]):
    # format uuids are unique
    format_uuids: dict[str, str] = dict()
    for format_result in check_format_results:
        if (
            len(format_result.errors) == 0
            and "manifest_uuid" in format_result.options
            and format_result.options["manifest_uuid"] in format_uuids
        ):
            format_result.errors.append(
                f"format have the same uuid ({format_result.options['manifest_uuid']}) "
                f"than format {format_uuids[format_result.options['manifest_uuid']]}"
            )

            format_uuids[format_result.options["manifest_uuid"]] = format_result.options.get(
                "manifest_uuid", "unknown"
            )

    # format slugs are unique
    format_slugs: dict[str, str] = dict()
    for format_result in check_format_results:
        if (
            len(format_result.errors) == 0
            and "manifest_slug" in format_result.options
            and format_result.options["manifest_slug"] in format_slugs
        ):
            format_result.errors.append(
                f"format have the same slug ({format_result.options['manifest_slug']}) "
                f"than format {format_slugs[format_result.options['manifest_slug']]}"
            )

            format_slugs[format_result.options["manifest_slug"]] = format_result.options.get(
                "manifest_slug", "unknown"
            )


def check_module(path: Path, args: argparse.Namespace) -> CheckResult:
    valid = ModuleValidator(path, args)
    valid.validate()

    return valid.result


def main():
    parser = argparse.ArgumentParser(description="Check formats")
    parser.add_argument("--changes", action="store_true", help="Only check modified formats and modules")
    parser.add_argument(
        "--ignore_missing_parsers",
        action="store_true",
        help="Ignore missing parser.yml",
    )
    parser.add_argument(
        "--ignore_event_fieldset_errors",
        action="store_true",
        help="Ignore missing or incorrect event.type and event.category in parser and tests",
    )
    parser.add_argument(
        "--ignore_missing_tests",
        action="store_true",
        help="Ignore missing tests folder",
    )
    parser.add_argument(
        "--ignore_empty_descriptions",
        action="store_true",
        help="Ignore empty, but existing descriptions",
    )
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    modules = find_modules(INTAKES_PATH)
    intake_formats = None

    if args.changes:
        result = subprocess.run(["git", "diff", "--name-only", "origin/main"], capture_output=True)
        changed_modules = set()
        changed_formats = set()
        for changed_file in result.stdout.splitlines():
            changed_file = changed_file.decode()
            parts = changed_file.split("/")

            if "utils/checks/" in changed_file:
                # to see all results whenever we change a code for the compliance check
                changed_modules = set(modules)
                changed_formats = set()
                break

            elif parts[0].startswith("."):
                continue

            if len(parts) > 2:
                changed_modules.add(parts[0])
                changed_formats.add(parts[1])

        modules = list(changed_modules)
        intake_formats = list(changed_formats)

    check_module_results = [check_module(INTAKES_PATH / module, args) for module in modules]
    check_module_uuids_and_slugs(check_module_results)

    check_format_results = []
    for check_module_result in check_module_results:
        check_format_results.extend(check_module_formats(check_module_result, intake_formats, args))
    check_format_uuids_and_slugs(check_format_results)

    in_error = False
    module_errors = []
    for res in check_module_results:
        if len(res.errors) > 0:
            in_error = True
            module_errors.append(res)

    format_errors = []
    for res in check_format_results:
        if len(res.errors) > 0:
            in_error = True
            format_errors.append(res)

    if args.json:
        results = {
            "modules": [
                {
                    "path": str(res.options["path"].relative_to(INTAKES_PATH)),
                    "errors": res.errors,
                }
                for res in module_errors
            ],
            "formats": [
                {
                    "path": str(res.options["path"].relative_to(INTAKES_PATH)),
                    "errors": res.errors,
                }
                for res in format_errors
            ],
        }
        print(json.dumps(results, indent=2))
    else:
        print(
            f"🔎 {len(check_module_results)} module(s) found: %s"
            % ",".join([str(module).replace(str(INTAKES_PATH), "") for module in modules])
        )
        for res in module_errors:
            module_name = res.options.get("path").relative_to(INTAKES_PATH)
            for error in res.errors:
                print(f"Module: {module_name} Error: {error}")

        print(
            f"🔎 {len(check_format_results)} format(s) found: %s"
            % ",".join([item.options.get("path").name for item in check_format_results])
        )
        for res in format_errors:
            format_path = res.options.get("path").relative_to(INTAKES_PATH)
            for error in res.errors:
                print(f"Format: {format_path} Error: {error}")

    if in_error:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
