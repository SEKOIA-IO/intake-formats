import argparse
import os
import re

import yaml

from . import Validator
from .constants import CheckResult


class ManifestValidator(Validator):
    """
    Check the module has a proper manifest
    """

    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        if not result.options.get("meta_dir"):
            return

        module_meta_dir = result.options["meta_dir"]
        module_manifest_file = os.path.join(module_meta_dir, "manifest.yml")

        check_manifest(manifest_file_path=module_manifest_file, result=result)


def check_manifest(manifest_file_path: str, result: CheckResult) -> None:
    if not os.path.isfile(manifest_file_path):
        result.errors.append(f"manifest file (`{manifest_file_path}`) is missing")
        return

    # check the format has a valid manifest
    try:
        with open(manifest_file_path, "r") as fd:
            manifest_content = yaml.safe_load(fd)

    except Exception as any_error:
        result.errors.append(f"manifest file cannot be loaded (`{any_error}`)")
        return

    result.options["manifest_file_path"] = manifest_file_path

    # check format has a uuid
    format_uuid = manifest_content.get("uuid")
    if not format_uuid:
        result.errors.append("no uuid found in the manifest file")

    else:
        result.options[f"manifest_uuid"] = format_uuid

    # check format has a name
    format_name = manifest_content.get("name")
    if not format_name:
        result.errors.append("no name found in the manifest file")

    else:
        result.options[f"manifest_name"] = format_name

    # check format has a slug
    format_slug = manifest_content.get("slug")
    if not format_slug:
        result.errors.append("no slug found in the manifest file")

    elif not re.match(r"^[a-z]([a-z]|-|\d)*$", format_slug):
        result.errors.append("incorrect slug in the manifest file")

    else:
        result.options[f"manifest_slug"] = format_slug
