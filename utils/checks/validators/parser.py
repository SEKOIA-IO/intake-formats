import argparse
import functools
import itertools
import json
import os
from typing import Any

import yaml

from . import Validator
from .constants import (CheckResult, CustomField, DeleteAction, IntakeFormat,
                        SetAction, TranslateAction)


class ParserValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        format_path = result.options["path"]
        parser_file = os.path.join(format_path, "ingest", "parser.yml")
        if not os.path.exists(parser_file):
            if not args.ignore_missing_parsers:
                result.errors.append(f"Parser file does not exist")

            return

        try:
            with open(parser_file, "r") as fd:
                parser = yaml.safe_load(fd)

            parser_content = IntakeFormat.model_validate(parser)

        except Exception as any_error:
            result.errors.append(
                f"parser file ({parser_file}) exists but cannot be loaded (`{any_error}`)"
            )
            return

        module_result = result.options["module_result"]
        taxonomy_exists_but_failed = result.options["taxonomy_exists_but_failed"]
        taxonomy_content = result.options["taxonomy"]

        check_format_parser(
            result,
            parser=parser_content,
            # Don't report undeclared fields for an incorrect taxonomy
            report_undeclared_fields=not taxonomy_exists_but_failed,
            ignore_event_fieldset_errors=args.ignore_event_fieldset_errors,
            format_taxonomy=taxonomy_content,
            module_taxonomy=module_result.options.get("taxonomy"),
        )


def check_format_parser(
    result: CheckResult,
    parser: IntakeFormat,
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
        item.name
        for item in itertools.chain(format_taxonomy.values(), module_taxonomy.values())
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
        non_declared_fields = {
            item for item in non_declared_fields if not item.startswith(f"{field}.")
        }

    if len(non_declared_fields) > 0 and report_undeclared_fields:
        for field in non_declared_fields:
            result.errors.append(
                f"Custom field `{field}` needs to be defined in _meta/fields.yml"
            )

    # Check whether event.type and event.category are set
    if not ignore_event_fieldset_errors:
        required_fields = {"event.type", "event.category"}
        for field in required_fields:
            if field not in used_fields:
                result.errors.append(f"Required field `{field}` was not set")

        if "event.category" in field_assignments:
            if not check_event_category_or_type(field_assignments["event.category"]):
                result.errors.append(f"event.category is not a list")

        if "event.type" in field_assignments:
            if not check_event_category_or_type(field_assignments["event.type"]):
                result.errors.append(f"event.type is not a list")

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


def check_event_category_to_type_mapping(
    event_categories: list[str], event_types: list[str]
):
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
        "utils/checks/validators/data/built_in_fields.txt",
        "rt",
    ) as f:
        builtin_fields = f.read().split("\n")

    with open(
        "utils/checks/validators/data/sekoiaio_flat.yml",
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
