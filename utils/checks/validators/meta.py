import argparse
import os

from . import Validator
from .constants import CheckResult


class MetaValidator(Validator):
    """
    check the module has a _meta directory
    """

    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        path = result.options.get("path")

        module_meta_dir = os.path.join(path, "_meta")
        if not os.path.isdir(module_meta_dir):
            result.errors.append(f"Meta directory(`{module_meta_dir}`) is missing")
            return

        result.options["meta_dir"] = module_meta_dir
