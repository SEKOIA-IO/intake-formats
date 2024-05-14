import argparse
from abc import ABC
from pathlib import Path

from .constants import CheckResult

INTAKES_PATH = Path(__file__).parent.parent.parent.parent


class Validator(ABC):
    """
    Every validator class changes mutable `result` data class either by adding data for the downstream validators
    or enhancing list of detected errors
    """

    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        raise NotImplementedError
