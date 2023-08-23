import argparse
import os

from . import Validator
from .constants import CheckResult


class ChangelogValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        format_path = result.options.get("path")

        changelog_path = os.path.join(format_path, "CHANGELOG.md")
        if not os.path.isfile(changelog_path):
            result.errors.append("CHANGELOG.md does not exist")
