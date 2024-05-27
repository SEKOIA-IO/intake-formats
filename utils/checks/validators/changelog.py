import argparse
import os
from pathlib import Path

from . import Validator
from .constants import CheckResult


class ChangelogValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        format_path: Path = result.options.get("path")

        changelog_path = format_path / "CHANGELOG.md"
        if not changelog_path.is_file():
            result.errors.append("CHANGELOG.md does not exist")
