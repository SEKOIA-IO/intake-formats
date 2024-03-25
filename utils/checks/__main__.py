import argparse
import os
import subprocess
import sys

from validators.constants import CheckResult
from validators.format import FormatValidator
from validators.module import ModuleValidator


def find_modules(root_path: str) -> list[str]:
    """
    Return the path to all the potential modules
    """
    module_paths: list[str] = []

    filtered_elements = {".git", ".github", "doc", "utils", ".idea"}

    for element in os.listdir(root_path):
        if element not in filtered_elements:
            element_path = os.path.join(root_path, element)
            if os.path.isdir(element_path):
                module_paths.append(element_path)

    return sorted(module_paths)


def find_formats(root_path: str, formats: list[str] | None = None) -> list[str]:
    """
    Return the path to all the potential formats
    """
    format_paths: list[str] = list()

    filtered_elements = {"_meta"}

    for element in os.listdir(root_path):
        if element not in filtered_elements:
            element_path = os.path.join(root_path, element)
            if os.path.isdir(element_path):
                if formats:
                    if element not in formats:
                        continue

                format_paths.append(element_path)

    return sorted(format_paths)


def check_format(
    path: str, module_result: CheckResult, args: argparse.Namespace
) -> CheckResult:
    valid = FormatValidator(path=path, module_result=module_result, args=args)
    valid.validate()

    return valid.result


def check_module_formats(
    module_result: CheckResult, formats: list[str] | None, args: argparse.Namespace
) -> list[CheckResult]:
    module_formats = find_formats(module_result.options["path"], formats=formats)
    print("module_formats", module_formats)

    result = [
        check_format(path=module_format, module_result=module_result, args=args)
        for module_format in module_formats
    ]

    return result


def check_module_uuids_and_slugs(check_module_results: list[CheckResult]):
    # module uuids are unique
    module_uuids: dict[str, str] = dict()
    for module_result in check_module_results:
        if (
            len(module_result.errors) == 0
            and "manifest_slug" in module_result.options
            and module_result.options["manifest_uuid"] in module_uuids
        ):
            module_result.errors.append(
                f"module have the same uuid ({module_result.options['manifest_uuid']}) "
                f"than module {module_uuids[module_result.options['manifest_uuid']]}"
            )

            module_uuids[
                module_result.options["manifest_uuid"]
            ] = module_result.options.get("manifest_slug", "unknown")

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

            module_slugs[
                module_result.options["manifest_slug"]
            ] = module_result.options.get("manifest_slug", "unknown")


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

            format_uuids[
                format_result.options["format_uuid"]
            ] = format_result.options.get("manifest_slug", "unknown")

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

            format_slugs[
                format_result.options["manifest_slug"]
            ] = format_result.options.get("manifest_slug", "unknown")


def check_module(path: str, args: argparse.Namespace) -> CheckResult:
    valid = ModuleValidator(path, args)
    valid.validate()

    return valid.result


def main():
    parser = argparse.ArgumentParser(description="Check formats")
    parser.add_argument(
        "--changes", action="store_true", help="Only check modified formats and modules"
    )
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
    args = parser.parse_args()

    modules = find_modules(".")
    intake_formats = None

    if args.changes:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main"], capture_output=True
        )
        changed_modules = set()
        changed_formats = set()
        for changed_file in result.stdout.splitlines():
            changed_file = changed_file.decode()
            parts = changed_file.split("/")

            if parts[-1] in ["conftest.py", "test_formats.py"]:
                break

            if len(parts) > 2 and parts[0] != "utils":
                changed_modules.add(parts[0])
                changed_formats.add(parts[1])

        modules = list(changed_modules)
        intake_formats = list(changed_formats)

    in_error = False

    check_module_results = [check_module(module, args) for module in modules]
    check_module_uuids_and_slugs(check_module_results)

    print(f"🔎 {len(check_module_results)} modules found")
    for res in check_module_results:
        if len(res.errors) > 0:
            in_error = True
            module_name = os.path.basename(res.options.get("path"))
            for error in res.errors:
                print(f"Module: {module_name} Error: {error}")

    check_format_results = []
    for check_module_result in check_module_results:
        check_format_results.extend(
            check_module_formats(check_module_result, intake_formats, args)
        )
    check_format_uuids_and_slugs(check_format_results)

    print(f"🔎 {len(check_format_results)} formats found")
    for res in check_format_results:
        if len(res.errors) > 0:
            in_error = True
            format_path = res.options.get("path")
            for error in res.errors:
                print(f"Format: {format_path} Error: {error}")

    if in_error:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
