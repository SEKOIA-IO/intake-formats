import json
import os
import re

import yaml

from constants import CheckResult, IntakeFormat, SmartDescription, TestFile
from helpers import (check_event_category_to_type_mapping, check_format_parser,
                     check_logo_image, check_manifest, check_taxonomy_file,
                     find_tests)


def check_format(format_path: str, module_result: CheckResult) -> CheckResult:
    result = CheckResult(
        name=f"check_format_{format_path}",
        description="Checks the format has a proper definition",
    )

    result.options["format_path"] = format_path
    result.options["module_path"] = module_result.options.get("module_path")

    # check the format has a _meta directory
    format_meta_dir = os.path.join(format_path, "_meta")
    if not os.path.isdir(format_meta_dir):
        result.errors.append(f"Meta directory(`{format_meta_dir}`) is missing")
        return result

    # check the format has a manifest file
    format_manifest_file = os.path.join(format_meta_dir, "manifest.yml")
    result = check_manifest(format_manifest_file, result)

    # check the format has a proper logo file
    format_logo_file = os.path.join(format_meta_dir, "logo.png")
    result = check_logo_image(result=result, image_path=format_logo_file)

    taxonomy_file = os.path.join(format_meta_dir, "fields.yml")
    result, taxonomy_content, taxonomy_exists_but_failed = check_taxonomy_file(
        taxonomy_file_path=taxonomy_file,
        result=result,
        for_module=False
    )

    # if format has a parser file, check its definition
    parser_file = os.path.join(format_path, "ingest", "parser.yml")
    if not os.path.isfile(parser_file):
        result.errors.append(f"Parser file does not exist")
        return result

    try:
        with open(parser_file, "r") as fd:
            parser = yaml.safe_load(fd)

        parser_content = IntakeFormat.model_validate(parser)

    except Exception as any_error:
        result.errors.append(
            f"parser file ({parser_file}) exists but cannot be loaded (`{any_error}`)"
        )
        return result

    result = check_format_parser(
        result,
        parser=parser_content,
        # Don't report undeclared fields for an incorrect taxonomy
        report_undeclared_fields=not taxonomy_exists_but_failed,
        format_taxonomy=taxonomy_content,
        module_taxonomy=module_result.options.get("module_taxonomy"),
    )

    # move to a separate function
    test_folder = os.path.join(format_path, "tests")
    if not os.path.exists(test_folder):
        result.errors.append("tests folder does not exist")
        return result

    test_paths = find_tests(test_folder)
    if len(test_paths) == 0:
        result.errors.append("no test found")
        return result

    for test_path in test_paths:
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

            if "event" in test_parsed.expected:
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

            else:
                result.errors.append(
                    f"No event.category and event.type declared as `expected` in {test_path}"
                )

        except Exception as any_error:
            print(any_error.with_traceback())
            result.errors.append(
                f"test {test_path} exists, but cannot be loaded (`{any_error}`)"
            )

    # Check smart descriptions
    smart_desc_file = os.path.join(format_meta_dir, "smart_descriptions.json")
    if not os.path.isfile(smart_desc_file):
        result.errors.append(f"smart-descriptions.json does not exist")

    else:
        try:
            with open(parser_file, "r") as fd:
                smart_desc = json.load(fd)

            smart_descriptions_content = [
                SmartDescription(**item) for item in smart_desc
            ]

        except Exception as any_error:
            result.errors.append(
                f"smart-descriptions.json exists, but cannot be loaded (`{any_error}`)"
            )

    # Check if CHANGELOG.md exists
    changelog_path = os.path.join(format_path, "CHANGELOG.md")
    if not os.path.isfile(changelog_path):
        result.errors.append("CHANGELOG.md does not exist")

    return result
