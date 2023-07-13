import functools
import itertools
import json
import os.path
import re
from typing import Any

import yaml

from constants import (CheckResult, CustomField, DeleteAction, IntakeFormat,
                       SetAction, TranslateAction)


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


def find_formats(root_path: str) -> list[str]:
    """
    Return the path to all the potential formats
    """
    format_paths: list[str] = list()

    filtered_elements = {"_meta"}

    for element in os.listdir(root_path):
        if element not in filtered_elements:
            element_path = os.path.join(root_path, element)
            if os.path.isdir(element_path):
                format_paths.append(element_path)

    return sorted(format_paths)


def find_tests(tests_path: str) -> set[str]:
    result: set[str] = set()

    for element in os.listdir(tests_path):
        if element.endswith(".json"):
            result.add(os.path.join(tests_path, element))

    return result


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

    # Check whether event.type event.kind event.categories are set
    if not ignore_event_fieldset_errors:
        required_fields = {"event.type", "event.kind", "event.category"}
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
    with open("utils/checks/data/built_in_fields.txt", "rt") as f:
        builtin_fields = f.read().split("\n")

    with open("utils/checks/data/sekoiaio_flat.yml", "rt") as f:
        sekoia_flat = yaml.safe_load(f)
        sekoia_fields = set(sekoia_flat.keys())

    result = set(builtin_fields).union(sekoia_fields)
    return result


def get_assigned_fields(parser: IntakeFormat) -> tuple[set[str], dict[str, Any]]:
    """
    Gather fields we affect in a parser
    """
    pipeline_steps = set(item.name for item in parser.pipeline)

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
                fields = set(action.mapping.keys())
                fields.update(set(action.mapping.values()))

                # could mention an ECS var or a runtime var, and we have to ignore the latter.
                # so we filter out fields with pipeline stage name in them (e.g. `parse_date.message`)
                fields = {
                    item for item in fields if item.split(".")[0] not in pipeline_steps
                }
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


def check_manifest(manifest_file_path: str, result: CheckResult) -> CheckResult:
    if not os.path.isfile(manifest_file_path):
        result.errors.append(f"manifest file (`{manifest_file_path}`) is missing")
        return result

    # check the format has a valid manifest
    try:
        with open(manifest_file_path, "r") as fd:
            manifest_content = yaml.safe_load(fd)

    except Exception as any_error:
        result.errors.append(f"manifest file cannot be loaded (`{any_error}`)")
        return result

    # check format has a uuid
    format_uuid = manifest_content.get("uuid")
    if not format_uuid:
        result.errors.append("no uuid found in the manifest file")

    else:
        result.options["format_uuid"] = format_uuid

    # check format has a name
    format_name = manifest_content.get("name")
    if not format_name:
        result.errors.append("no name found in the manifest file")

    else:
        result.options["format_name"] = format_name

    # check format has a slug
    format_slug = manifest_content.get("slug")
    if not format_slug:
        result.errors.append("no slug found in the manifest file")

    elif not re.match(r"^[a-z]([a-z]|-|\d)*$", format_slug):
        result.errors.append("incorrect slug in the manifest file")

    else:
        result.options["format_slug"] = format_slug

    return result


def check_logo_image(result: CheckResult, image_path: str):
    from PIL import Image

    def has_transparency(img: Image):
        if img.info.get("transparency", None) is not None:
            return True

        elif img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True

        elif img.mode == "RGBA":
            extrema = img.getextrema()
            if extrema[3][0] < 255:
                return True

        return False

    if not os.path.isfile(image_path):
        result.errors.append(f"Logofile (`{image_path}`) is missing")
        return result

    image = Image.open(image_path)
    if image.format != "PNG":
        result.errors.append("Logo is not in PNG format")

    if image.width != image.height:
        result.errors.append(f"Logo is not square - {image.width}x{image.height}px")

    if not has_transparency(image):
        result.errors.append("Logo background is not transparent")

    if os.path.getsize(image_path) > 50 * 1024:
        result.errors.append("Logo file weights more than 50 KiB")

    image.close()
    return result


def check_taxonomy_file(
    taxonomy_file_path: str, result: CheckResult, for_module: bool = False
) -> tuple[CheckResult, dict[str, CustomField] | None, bool]:
    exists_but_failed = False

    if not os.path.isfile(taxonomy_file_path):
        if not for_module:
            result.errors.append(
                "No format taxonomy found. Please create _meta/fields.yml"
            )

        return result, None, exists_but_failed

    if os.path.getsize(taxonomy_file_path) == 0:
        # File is empty
        return result, None, exists_but_failed

    try:
        with open(taxonomy_file_path, "r") as fd:
            taxonomy = yaml.safe_load(fd)

        taxonomy_content = {
            item_key: CustomField(**item_value)
            for item_key, item_value in taxonomy.items()
        }

    except Exception as any_error:
        result.errors.append(f"Taxonomy file cannot be loaded (`{any_error}`)")
        exists_but_failed = True

        return result, None, exists_but_failed

    return result, taxonomy_content, exists_but_failed
