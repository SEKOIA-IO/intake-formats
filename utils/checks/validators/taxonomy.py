import argparse
import os

import yaml

from . import Validator
from .constants import CheckResult, CustomField


class TaxonomyValidator(Validator):
    FOR_MODULE = False

    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        if not result.options.get("meta_dir"):
            return

        module_meta_dir = result.options["meta_dir"]
        taxonomy_file = os.path.join(module_meta_dir, "fields.yml")
        taxonomy_content, exists_but_failed = check_taxonomy_file(
            taxonomy_file_path=taxonomy_file, result=result, for_module=cls.FOR_MODULE
        )
        result.options["taxonomy"] = taxonomy_content
        result.options["taxonomy_exists_but_failed"] = exists_but_failed


class ModuleTaxonomyValidator(TaxonomyValidator):
    FOR_MODULE = True


def check_taxonomy_file(
    taxonomy_file_path: str, result: CheckResult, for_module: bool = False
) -> tuple[dict[str, CustomField] | None, bool]:
    exists_but_failed = False

    if not os.path.isfile(taxonomy_file_path):
        if not for_module:
            result.errors.append("No format taxonomy found. Please create _meta/fields.yml")

        return None, exists_but_failed

    if os.path.getsize(taxonomy_file_path) == 0:
        # File is empty
        return None, exists_but_failed

    try:
        with open(taxonomy_file_path, "r") as fd:
            taxonomy = yaml.safe_load(fd)

        taxonomy_content = {item_key: CustomField(**item_value) for item_key, item_value in taxonomy.items()}

    except Exception as any_error:
        result.errors.append(f"Taxonomy file cannot be loaded (`{any_error}`)")
        exists_but_failed = True

        return None, exists_but_failed

    return taxonomy_content, exists_but_failed
