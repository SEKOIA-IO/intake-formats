import argparse
from pathlib import Path

from . import INTAKES_PATH, Validator
from .constants import CheckResult


class MetaValidator(Validator):
    """
    check the module has a _meta directory
    """

    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        path: Path = result.options.get("path")

        module_meta_dir = path / "_meta"
        if not module_meta_dir.is_dir():
            result.errors.append(f"Meta directory(`{module_meta_dir.relative_to(INTAKES_PATH)}`) is missing")
            return

        result.options["meta_dir"] = module_meta_dir
