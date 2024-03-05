import argparse
from abc import ABC

from .constants import CheckResult


class Validator(ABC):
    """
    Every validator class changes mutable `result` data class either by adding data for the downstream validators
    or enhancing list of detected errors
    """

    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        raise NotImplementedError
