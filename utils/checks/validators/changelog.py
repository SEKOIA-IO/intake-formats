import argparse
from pathlib import Path

from . import Validator, INTAKES_PATH
from .constants import CheckResult, ValidationError


class ChangelogValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        format_path: Path = result.options.get("path")

        changelog_path = format_path / "CHANGELOG.md"
        if not changelog_path.is_file():
            result.errors.append(
                ValidationError(message="CHANGELOG.md does not exist", file_path=str(changelog_path.relative_to(INTAKES_PATH)))
            )
