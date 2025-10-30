import argparse
import functools
import itertools
import json
from pathlib import Path
from typing import Any

import yaml

from . import INTAKES_PATH, Validator
from .constants import (
    CheckResult,
    CustomField,
    DeleteAction,
    IntakeFormat,
    SetAction,
    TranslateAction,
    ValidationError,
)


class ParserFieldError(ValidationError):
    message: str
    code: str
    file_path: str
    field_name: str

    def __str__(self) -> str:
        return f"{self.message} field=`{self.field_name}` file_path=`{self.file_path}`"


class ParserValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        format_path: Path = result.options["path"]
        parser_file = format_path / "ingest" / "parser.yml"
        if not parser_file.exists():
            if not args.ignore_missing_parsers:
                result.errors.append(
                    ValidationError(
                        message="Parser file does not exist",
                        file_path=str(parser_file.relative_to(INTAKES_PATH)),
                        code="parser_missing",
                    )
                )

            return

        try:
            with open(parser_file, "r") as fd:
                parser = yaml.safe_load(fd)

            parser_content = IntakeFormat.model_validate(parser)

        except Exception as any_error:
            result.errors.append(
                ValidationError(
                    message="parser file exists but cannot be loaded",
                    file_path=str(parser_file.relative_to(INTAKES_PATH)),
                    error=str(any_error),
                    code="parser_invalid",
                )
            )
            return

        module_result = result.options["module_result"]
        taxonomy_exists_but_failed = result.options["taxonomy_exists_but_failed"]
        taxonomy_content = result.options["taxonomy"]

        check_format_parser(
            result,
            parser=parser_content,
            parser_file=parser_file,
            # Don't report undeclared fields for an incorrect taxonomy
            report_undeclared_fields=not taxonomy_exists_but_failed,
            ignore_event_fieldset_errors=args.ignore_event_fieldset_errors,
            format_taxonomy=taxonomy_content,
            module_taxonomy=module_result.options.get("taxonomy"),
        )


def check_format_parser(
    result: CheckResult,
    parser: IntakeFormat,
    parser_file: Path,
    report_undeclared_fields: bool = True,
    ignore_event_fieldset_errors: bool = False,
    format_taxonomy: dict[str, CustomField] | None = None,
    module_taxonomy: dict[str, CustomField] | None = None,
) -> CheckResult:
    if not format_taxonomy:
        format_taxonomy = {}

    if not module_taxonomy:
        module_taxonomy = {}

    # Fields we declared in fields.yml either on a format or on a module level
    declared_custom_fields = {
        item.name for item in itertools.chain(format_taxonomy.values(), module_taxonomy.values())
    }

    # `object`-type field can have arbitrary properties
    object_fields = {
        item.name
        for item in itertools.chain(format_taxonomy.values(), module_taxonomy.values())
        if item.type == "object"
    }

    # Fields defined in ECS
    builtin_fields = get_builtin_fields()

    # All fields that declared somewhere
    declared_fields = expand_fields(declared_custom_fields.union(builtin_fields))

    # Fields assigned in a parser
    used_fields, field_assignments = get_assigned_fields(parser)

    # Find fields that not declared anywhere
    non_declared_fields = used_fields.difference(declared_fields)

    # Filter out `object`-type fields from non-declared - they can have arbitrary properties
    for field in object_fields:
        non_declared_fields = {item for item in non_declared_fields if not item.startswith(f"{field}.")}

    if len(non_declared_fields) > 0 and report_undeclared_fields:
        for field in non_declared_fields:
            result.errors.append(
                ParserFieldError(
                    message="Custom field needs to be defined in _meta/fields.yml",
                    file_path=str(parser_file.relative_to(INTAKES_PATH)),
                    field_name=field,
                    code="parser_field_undeclared",
                )
            )

    # Check whether event.type and event.category are set
    if not ignore_event_fieldset_errors:
        required_fields = {"event.type", "event.category"}
        for field in required_fields:
            if field not in used_fields:
                result.errors.append(
                    ParserFieldError(
                        message="Required field was not set",
                        file_path=str(parser_file.relative_to(INTAKES_PATH)),
                        field_name=field,
                        code="parser_field_required_missing",
                    )
                )

        if "event.category" in field_assignments and not check_event_category_or_type(
            field_assignments["event.category"]
        ):
            result.errors.append(
                ValidationError(
                    message="event.category is not a list",
                    file_path=str(parser_file.relative_to(INTAKES_PATH)),
                    code="parser_event_category_not_list",
                )
            )

        if "event.type" in field_assignments and not check_event_category_or_type(field_assignments["event.type"]):
            result.errors.append(
                ValidationError(
                    message="event.type is not a list",
                    file_path=str(parser_file.relative_to(INTAKES_PATH)),
                    code="parser_event_type_not_list",
                )
            )

    return result


def check_event_category_or_type(field_var: str) -> bool:
    if type(field_var) == list:
        return True

    elif field_var.startswith("{{") and field_var.endswith("}}"):
        # can't properly check this, assume it's ok - will rely on checking test files instead
        return True

    else:
        try:
            field = json.loads(field_var)

            if type(field) == list:
                return True

        except json.decoder.JSONDecodeError:
            return False

    return False


def check_event_category_to_type_mapping(event_categories: list[str], event_types: list[str]):
    ecs_categories = {
        "authentication",
        "configuration",
        "database",
        "driver",
        "email",
        "file",
        "host",
        "iam",
        "intrusion_detection",
        "malware",
        "network",
        "package",
        "process",
        "registry",
        "session",
        "threat",
        "vulnerability",
        "web",
    }

    ecs_event_category_to_type = {
        "authentication": ["start", "end", "info"],
        "configuration": ["access", "change", "creation", "deletion", "info"],
        "database": ["access", "change", "info", "error"],
        "driver": ["change", "end", "info", "start"],
        "email": ["info"],
        "file": ["change", "creation", "deletion", "info"],
        "host": ["access", "change", "end", "info", "start"],
        "iam": ["admin", "change", "creation", "deletion", "group", "info", "user"],
        "intrusion_detection": ["allowed", "denied", "info"],
        "malware": ["info"],
        "network": [
            "access",
            "allowed",
            "connection",
            "denied",
            "end",
            "info",
            "protocol",
            "start",
        ],
        "package": ["access", "change", "deletion", "info", "installation", "start"],
        "process": ["access", "change", "end", "info", "start"],
        "registry": ["access", "change", "creation", "deletion"],
        "session": ["start", "end", "info"],
        "threat": ["indicator"],
        "vulnerability": ["info"],
        "web": ["access", "error", "info"],
    }

    allowed_types = set()
    for category in event_categories:
        if category not in ecs_categories:
            return False

        allowed_types.update(ecs_event_category_to_type[category])

    for event_type in event_types:
        if event_type not in allowed_types:
            return False

    return True


@functools.cache
def get_builtin_fields() -> set[str]:
    with open(
        INTAKES_PATH / "utils/checks/validators/data/built_in_fields.txt",
        "rt",
    ) as f:
        builtin_fields = f.read().split("\n")

    with open(
        INTAKES_PATH / "utils/checks/validators/data/sekoiaio_flat.yml",
        "rt",
    ) as f:
        sekoia_flat = yaml.safe_load(f)
        sekoia_fields = set(sekoia_flat.keys())

    result = set(builtin_fields).union(sekoia_fields)
    return result


def get_assigned_fields(parser: IntakeFormat) -> tuple[set[str], dict[str, Any]]:
    """
    Gather fields we affect in a parser
    """
    field_names: set[str] = set()
    set_fields: dict[str, str] = {}

    for stage_name, stage in parser.stages.items():
        for action in stage.actions:
            if isinstance(action, SetAction):
                # direct assignment
                field_names.update(action.set.keys())
                for var_name, var_value in action.set.items():
                    field_names.add(var_name)
                    set_fields[var_name] = var_value

            elif isinstance(action, DeleteAction):
                field_names.update(action.delete)

            elif isinstance(action, TranslateAction):
                # only values(), because keys() could involve a runtime var
                # this way we could get false negatives, but will avoid all false positives
                fields = set(action.mapping.values())
                field_names.update(fields)

    return field_names, set_fields


def expand_fields(fields: set[str]):
    """
    If there's fieldset sharing the same prefix, it's possible to assign JSON with the same structure to the
    whole fieldset just using prefix. For instance,
    ```
    dll: "{{json.event.dll}}"
    ```
    Where json.event.dll would be
    ```
    {"name": "runtime.dll", "path": "C:/Windows/system32"}
    ```
    Thus, we have to accept not only `dll.name` and `dll.path` as correct built-in fields, but `dll` as well.
    """
    result: set[str] = set()

    for field in fields:
        parts = field.split(".")
        result.add(field)

        for i in range(1, len(parts) + 1):
            result.add(".".join(parts[:i]))

    return result
