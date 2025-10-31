import argparse
import json
import re
from pathlib import Path

from . import INTAKES_PATH, Validator
from .constants import CheckResult, TestFile, ValidationError
from .parser import check_event_category_to_type_mapping


class TestFileValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        format_path: Path = result.options["path"]

        test_folder = format_path / "tests"
        if not test_folder.exists():
            if not args.ignore_missing_tests:
                result.errors.append(
                    ValidationError(
                        message="tests folder does not exist",
                        file_path=str(test_folder.relative_to(INTAKES_PATH)),
                        code="tests_missing",
                    )
                )
            return

        test_paths = find_tests(test_folder)
        if len(test_paths) == 0:
            if not args.ignore_missing_tests:
                result.errors.append(
                    ValidationError(
                        message="no test found",
                        file_path=str(test_folder.relative_to(INTAKES_PATH)),
                        code="tests_missing",
                    )
                )
            return

        for test_path in test_paths:
            check_test_file(
                test_path=test_path,
                ignore_event_fieldset_errors=args.ignore_event_fieldset_errors,
                result=result,
            )


def find_tests(tests_path: Path) -> list[Path]:
    result: list[Path] = []

    for element in tests_path.iterdir():
        if element.name.endswith(".json"):
            result.append(element)

    return result


def check_test_file(test_path: Path, ignore_event_fieldset_errors: bool, result: CheckResult) -> None:
    try:
        with open(test_path, "rt") as file:
            test_content = json.load(file)

        test_parsed = TestFile.model_validate(test_content)

        test_time_stamp = test_parsed.expected.get("@timestamp")
        re_rfc3339 = re.compile(r"^((?:(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})?)$")

        if test_time_stamp and not re.match(re_rfc3339, test_time_stamp):
            result.errors.append(
                ValidationError(
                    message="Incorrect @timestamp in the test",
                    file_path=str(test_path.relative_to(INTAKES_PATH)),
                    code="test_timestamp_incorrect",
                )
            )

        if "event" in test_parsed.expected and not ignore_event_fieldset_errors:
            event = test_parsed.expected["event"]

            event_type_readable = False
            event_category_readable = False

            if "type" in event:
                if type(event["type"]) != list:
                    result.errors.append(
                        ValidationError(
                            message="event.type is not a list",
                            file_path=str(test_path.relative_to(INTAKES_PATH)),
                            code="test_event_type_incorrect",
                        )
                    )
                else:
                    event_type_readable = True

            if "category" in event:
                if type(event["category"]) != list:
                    result.errors.append(
                        ValidationError(
                            message="event.category is not a list",
                            file_path=str(test_path.relative_to(INTAKES_PATH)),
                            code="test_event_category_incorrect",
                        )
                    )
                else:
                    event_category_readable = True

            if event_type_readable and event_category_readable:
                check_mapping = check_event_category_to_type_mapping(
                    event_categories=event["category"], event_types=event["type"]
                )
                if not check_mapping:
                    result.errors.append(
                        ValidationError(
                            message="`event.type` does not match the type associated to the `event.category`",
                            file_path=str(test_path.relative_to(INTAKES_PATH)),
                            code="test_event_category_type_mismatch",
                        )
                    )

        elif not ignore_event_fieldset_errors:
            result.errors.append(
                ValidationError(
                    message="No event.category and event.type declared as `expected`",
                    file_path=str(test_path.relative_to(INTAKES_PATH)),
                    code="test_event_fields_missing",
                )
            )

    except Exception as any_error:
        result.errors.append(
            ValidationError(
                message="test exists, but cannot be loaded",
                file_path=str(test_path.relative_to(INTAKES_PATH)),
                error=str(any_error),
                code="test_invalid",
            )
        )
