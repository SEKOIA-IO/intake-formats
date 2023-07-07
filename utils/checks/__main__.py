import sys

from constants import CheckResult
from format import check_format
from helpers import find_formats, find_modules
from module import check_module


def check_module_formats(module_result: CheckResult) -> list[CheckResult]:
    module_formats = find_formats(module_result.options["module_path"])

    check_module_formats = [
        check_format(module_format, module_result) for module_format in module_formats
    ]

    return check_module_formats


def check_module_uuids_and_slugs(check_module_results: list[CheckResult]):
    # module uuids are unique
    module_uuids: dict[str, str] = dict()
    for module_result in check_module_results:
        if (
            len(module_result.errors) == 0
            and "module_slug" in module_result.options
            and module_result.options["module_uuid"] in module_uuids
        ):
            module_result.errors.append(
                f"module have the same uuid ({module_result.options['module_uuid']}) "
                f"than module {module_uuids[module_result.options['module_uuid']]}"
            )

            module_uuids[
                module_result.options["module_uuid"]
            ] = module_result.options.get("module_slug", "unknown")

    # module slugs are unique
    module_slugs: dict[str, str] = dict()
    for module_result in check_module_results:
        if (
            len(module_result.errors) == 0
            and "module_slug" in module_result.options
            and module_result.options["module_slug"] in module_slugs
        ):
            module_result.errors.append(
                f"module have the same slug ({module_result.options['module_slug']}) "
                f"than module {module_slugs[module_result.options['module_slug']]}"
            )

            module_slugs[
                module_result.options["module_slug"]
            ] = module_result.options.get("module_slug", "unknown")


def check_format_uuids_and_slugs(check_format_results: list[CheckResult]):
    # format uuids are unique
    format_uuids: dict[str, str] = dict()
    for format_result in check_format_results:
        if (
            len(format_result.errors) == 0
            and "format_uuid" in format_result.options
            and format_result.options["format_uuid"] in format_uuids
        ):
            format_result.errors.append(
                f"format have the same uuid ({format_result.options['format_uuid']}) "
                f"than format {format_uuids[format_result.options['format_uuid']]}"
            )

            format_uuids[
                format_result.options["format_uuid"]
            ] = format_result.options.get("format_slug", "unknown")

    # format slugs are unique
    format_slugs: dict[str, str] = dict()
    for format_result in check_format_results:
        if (
            len(format_result.errors) == 0
            and "format_slug" in format_result.options
            and format_result.options["format_slug"] in format_slugs
        ):
            format_result.errors.append(
                f"format have the same slug ({format_result.options['format_slug']}) "
                f"than format {format_slugs[format_result.options['format_slug']]}"
            )

            format_slugs[
                format_result.options["format_slug"]
            ] = format_result.options.get("format_slug", "unknown")


def main():
    modules = find_modules(".")

    in_error = False

    check_module_results = [check_module(module) for module in modules]
    check_module_uuids_and_slugs(check_module_results)

    print(f"🔎 {len(check_module_results)} modules found")
    for res in check_module_results:
        if len(res.errors) > 0:
            in_error = True
            module_path = res.options.get("module_path")
            for error in res.errors:
                print(f"Module: {module_path} Error: {error}")

    check_format_results = []
    for check_module_result in check_module_results:
        check_format_results.extend(check_module_formats(check_module_result))

    check_format_uuids_and_slugs(check_format_results)

    print(f"🔎 {len(check_format_results)} formats found")
    for res in check_format_results:
        if len(res.errors) > 0:
            in_error = True
            format_path = res.options.get("format_path")
            for error in res.errors:
                print(f"Format: {format_path} Error: {error}")

    if in_error:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
