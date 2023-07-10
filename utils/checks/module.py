import os

from constants import CheckResult
from helpers import check_logo_image, check_manifest, check_taxonomy_file


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
        result.errors.append(f"Meta directory(`{module_meta_dir}`) is missing")
        return result

    # check the module has a manifest file
    module_manifest_file = os.path.join(module_meta_dir, "manifest.yml")
    result = check_manifest(module_manifest_file, result)

    # check module taxonomy, if exist
    taxonomy_file = os.path.join(module_meta_dir, "fields.yml")
    result, taxonomy_content, _ = check_taxonomy_file(
        taxonomy_file_path=taxonomy_file, result=result, for_module=True
    )
    result.options["module_taxonomy"] = taxonomy_content

    logo_path = os.path.join(module_meta_dir, "logo.png")
    result = check_logo_image(result, logo_path)

    return result
