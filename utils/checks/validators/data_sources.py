import argparse
import functools

import yaml

from . import INTAKES_PATH, Validator
from .constants import CheckResult


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
            result.errors.append("no data sources found in the manifest file")
            return

        unsupported_data_sources = (
            set(item.lower() for item in format_data_sources.keys())
            - get_allowed_data_sources()
        )
        unsupported_data_sources_labels = [
            item
            for item in format_data_sources
            if item.lower() in unsupported_data_sources
        ]
        if len(unsupported_data_sources_labels) > 0:
            for data_source in unsupported_data_sources_labels:
                result.errors.append(f"Data source `{data_source}` is not supported")
            return


@functools.cache
def get_allowed_data_sources() -> set[str]:
    with open(
        INTAKES_PATH / "utils/checks/validators/data/data_sources.txt", "rt"
    ) as f:
        data_sources = set(item.lower() for item in f.read().split("\n"))

    return data_sources
