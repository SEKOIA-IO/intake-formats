import argparse
import functools

import yaml

from . import INTAKES_PATH, Validator
from .constants import CheckResult, ValidationError


class DataSourceValidationError(ValidationError):
    message: str
    code: str
    file_path: str
    data_source: str

    def __str__(self) -> str:
        return f"{self.message}: '{self.data_source}'"


class ManifestDataSourcesValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        manifest_file_path = result.options.get("manifest_file_path")
        if not manifest_file_path:
            return

        with open(manifest_file_path, "rt") as file:
            manifest_content = yaml.safe_load(file)

        format_data_sources = manifest_content.get("data_sources")
        if not format_data_sources:
            result.errors.append(
                ValidationError(
                    message="no data sources found in the manifest file",
                    file_path=str(manifest_file_path.relative_to(INTAKES_PATH)),
                    code="data_sources_missing",
                )
            )
            return

        unsupported_data_sources = (
            set(item.lower() for item in format_data_sources.keys()) - get_allowed_data_sources()
        )
        unsupported_data_sources_labels = [
            item for item in format_data_sources if item.lower() in unsupported_data_sources
        ]
        if len(unsupported_data_sources_labels) > 0:
            for data_source in unsupported_data_sources_labels:
                result.errors.append(
                    DataSourceValidationError(
                        message="Data source is not supported",
                        file_path=str(manifest_file_path.relative_to(INTAKES_PATH)),
                        data_source=data_source,
                        code="data_source_unsupported",
                    )
                )
            return


@functools.cache
def get_allowed_data_sources() -> set[str]:
    with open(INTAKES_PATH / "utils/checks/validators/data/data_sources.txt", "rt") as f:
        data_sources = set(item.lower() for item in f.read().split("\n"))

    return data_sources
