#!/usr/bin/env python3
# coding: utf-8

import os
import sys
from typing import Any, Dict, List, Optional, Set, Union

import yaml
from pydantic import BaseModel


class ExternalStageReference(BaseModel):
    name: str
    properties: Optional[Dict[str, Any]]


class StageReference(BaseModel):

    id: Optional[str]
    name: str
    external: Optional[ExternalStageReference]
    filter: Optional[str]


class Action(BaseModel):
    name: str = "unknown"
    filter: Optional[str]


class SetAction(Action):
    name: str = "set"
    set: Dict[str, Union[str, List[str]]]


class DeleteAction(Action):
    name: str = "delete"
    delete: List[str]


class TranslateAction(Action):
    name: str = "translate"
    dictionary: Dict[Any, Any]
    mapping: Dict[str, str]
    fallback: Optional[Any]


class Stage(BaseModel):

    description: Optional[str]
    actions: List[Union[SetAction, DeleteAction, TranslateAction]]


class IntakeFormat(BaseModel):

    name: str
    pipeline: List[StageReference]
    stages: Dict[str, Stage]


class CheckResult(BaseModel):
    name: str
    description: str
    error: Optional[str] = None
    warnings: List[str] = []
    options: Dict[str, Any] = dict()


def find_modules(root_path: str) -> Set[str]:
    """
    Return the path to all the potential modules
    """
    module_paths: Set[str] = set()

    filtered_elements = {".git", ".github", "doc", "utils"}

    for element in os.listdir(root_path):
        if element not in filtered_elements:
            element_path = os.path.join(root_path, element)
            if os.path.isdir(element_path):
                module_paths.add(element_path)

    return module_paths


def check_module(module_path: str) -> CheckResult:
    """
    Check the module is valid:
    - it has a unique identifier
    - it has a name
    - it has a unique slug
    """
    result = CheckResult(
        name=f"check_module_{module_path}",
        description="Checks the module has a proper definition",
    )

    result.options["module_path"] = module_path

    # check the module has a _meta directory
    module_meta_dir = os.path.join(module_path, "_meta")
    if not os.path.isdir(module_meta_dir):
        result.error = f"Meta directory(`{module_meta_dir}`) is missing"
        return result

    # check the module has a manifest file
    module_manifest_file = os.path.join(module_meta_dir, "manifest.yml")
    if not os.path.isfile(module_manifest_file):
        result.error = f"manifest file (`{module_manifest_file}`) is missing"
        return result

    # check the module has a valid manifest
    try:
        with open(module_manifest_file, "r") as fd:
            manifest_content = yaml.safe_load(fd)
    except Exception as any_error:
        result.error = f"manifest file cannot be loaded (`{any_error}`)"
        return result

    # check module has a uuid
    module_uuid = manifest_content.get("uuid")
    if not module_uuid:
        result.error = "no uuid found in the manifest file"
        return result
    result.options["module_uuid"] = module_uuid

    # check module has a name
    module_name = manifest_content.get("name")
    if not module_name:
        result.error = "no name found in the manifest file"
        return result
    result.options["module_name"] = module_name

    # check module has a slug
    module_slug = manifest_content.get("slug")
    if not module_slug:
        result.error = "no slug found in the manifest file"
        return result
    result.options["module_slug"] = module_slug

    return result


def check_module_uuids_and_slugs(check_module_results: List[CheckResult]):

    # module uuids are unique
    module_uuids: Dict[str, str] = dict()
    for module_result in check_module_results:
        if (
            not module_result.error
            and module_result.options["module_uuid"] in module_uuids
        ):
            module_result.error = (
                f"module have the same uuid ({module_result.options['module_uuid']}) "
                f"than module {module_uuids[module_result.options['module_uuid']]}"
            )

            module_uuids[
                module_result.options["module_uuid"]
            ] = module_result.options.get("module_slug", "unknown")

    # module slugs are unique
    module_slugs: Dict[str, str] = dict()
    for module_result in check_module_results:
        if (
            not module_result.error
            and module_result.options["module_slug"] in module_slugs
        ):
            module_result.error = (
                f"module have the same slug ({module_result.options['module_slug']}) "
                f"than module {module_slugs[module_result.options['module_slug']]}"
            )

            module_slugs[
                module_result.options["module_slug"]
            ] = module_result.options.get("module_slug", "unknown")


def check_format_uuids_and_slugs(check_format_results: List[CheckResult]):

    # format uuids are unique
    format_uuids: Dict[str, str] = dict()
    for format_result in check_format_results:
        if (
            not format_result.error
            and format_result.options["format_uuid"] in format_uuids
        ):
            format_result.error = (
                f"format have the same uuid ({format_result.options['format_uuid']}) "
                f"than format {format_uuids[format_result.options['format_uuid']]}"
            )

            format_uuids[
                format_result.options["format_uuid"]
            ] = format_result.options.get("format_slug", "unknown")

    # format slugs are unique
    format_slugs: Dict[str, str] = dict()
    for format_result in check_format_results:
        if (
            not format_result.error
            and format_result.options["format_slug"] in format_slugs
        ):
            format_result.error = (
                f"format have the same slug ({format_result.options['format_slug']}) "
                f"than format {format_slugs[format_result.options['format_slug']]}"
            )

            format_slugs[
                format_result.options["format_slug"]
            ] = format_result.options.get("format_slug", "unknown")


def find_formats(root_path: str) -> Set[str]:
    """
    Return the path to all the potential formats
    """
    format_paths: Set[str] = set()

    filtered_elements = {"_meta"}

    for element in os.listdir(root_path):
        if element not in filtered_elements:
            element_path = os.path.join(root_path, element)
            if os.path.isdir(element_path):
                format_paths.add(element_path)

    return format_paths


def check_format(format_path: str) -> CheckResult:
    """
    Check the format is valid:
    - it has a unique identifier
    - it has a name
    - it has a unique slug
    - it has a description
    """
    result = CheckResult(
        name=f"check_format_{format_path}",
        description="Checks the format has a proper definition",
    )

    result.options["format_path"] = format_path

    # check the format has a _meta directory
    format_meta_dir = os.path.join(format_path, "_meta")
    if not os.path.isdir(format_meta_dir):
        result.error = f"Meta directory(`{format_meta_dir}`) is missing"
        return result

    # check the format has a manifest file
    format_manifest_file = os.path.join(format_meta_dir, "manifest.yml")
    if not os.path.isfile(format_manifest_file):
        result.error = f"manifest file (`{format_manifest_file}`) is missing"
        return result

    # check the format has a valid manifest
    try:
        with open(format_manifest_file, "r") as fd:
            manifest_content = yaml.safe_load(fd)
    except Exception as any_error:
        result.error = f"manifest file cannot be loaded (`{any_error}`)"
        return result

    # check format has a uuid
    format_uuid = manifest_content.get("uuid")
    if not format_uuid:
        result.error = "no uuid found in the manifest file"
        return result
    result.options["format_uuid"] = format_uuid

    # check format has a name
    format_name = manifest_content.get("name")
    if not format_name:
        result.error = "no name found in the manifest file"
        return result
    result.options["format_name"] = format_name

    # check format has a slug
    format_slug = manifest_content.get("slug")
    if not format_slug:
        result.error = "no slug found in the manifest file"
        return result
    result.options["format_slug"] = format_slug

    # check the format has a manifest file
    format_logo_file = os.path.join(format_meta_dir, "logo.png")
    if not os.path.isfile(format_logo_file):
        result.error = f"Logofile (`{format_logo_file}`) is missing"
        return result

    # if format has a parser file, check its definition
    parser_file = os.path.join(format_path, "ingest/parser.yml")
    if os.path.isfile(parser_file):

        try:
            with open(parser_file, "r") as fd:
                parser = yaml.safe_load(fd)

            IntakeFormat.parse_obj(parser)

        except Exception as any_error:
            result.error = f"parser file ({parser_file}) exists but cannot be loaded (`{any_error}`)"
            return result
    return result


def check_module_formats(module_result: CheckResult) -> List[CheckResult]:

    module_formats = find_formats(module_result.options["module_path"])

    check_module_formats = [
        check_format(module_format) for module_format in module_formats
    ]

    return check_module_formats


def main():
    modules = find_modules(".")

    in_error = False

    check_module_results = [check_module(module) for module in modules]
    check_module_uuids_and_slugs(check_module_results)

    print(f"🔎 {len(check_module_results)} modules found")
    for res in check_module_results:
        if res.error:
            in_error = True
            print(res)

    check_format_results = []
    for check_module_result in check_module_results:
        check_format_results.extend(check_module_formats(check_module_result))
    check_format_uuids_and_slugs(check_format_results)

    print(f"🔎 {len(check_format_results)} formats found")
    for res in check_format_results:
        if res.error:
            in_error = True
            print(res)

    if in_error:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
