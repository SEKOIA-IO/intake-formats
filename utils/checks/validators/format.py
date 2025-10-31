import argparse
from pathlib import Path

from . import (
    ChangelogValidator,
    LogoValidator,
    ManifestDataSourcesValidator,
    ManifestValidator,
    MetaValidator,
    ParserValidator,
    TaxonomyValidator,
    TestFileValidator,
)
from .constants import CheckResult


class FormatValidator:
    def __init__(self, path: Path, module_result: CheckResult, args: argparse.Namespace) -> None:
        self.path = path

        format_name = path.name
        self.result = CheckResult(
            name=f"check_format_{format_name}",
            description="Checks the format has a proper definition",
            options={
                "path": path,
                "module_result": module_result,
                "module_path": module_result.options["path"],
            },
        )

        self.validators = [
            MetaValidator,
            LogoValidator,
            ManifestValidator,
            ManifestDataSourcesValidator,
            TaxonomyValidator,
            ParserValidator,
            TestFileValidator(args),
            ChangelogValidator,
        ]

        self.args = args

    def validate(self):
        for validator in self.validators:
            validator.validate(self.result, self.args)
