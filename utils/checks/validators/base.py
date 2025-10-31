import argparse
from abc import ABC
from pathlib import Path

from .constants import CheckResult

INTAKES_PATH = Path(__file__).parent.parent.parent.parent


class Validator(ABC):
    """
    Every validator class changes mutable `result` data class either by adding data for the downstream validators
    or enhancing list of detected errors

    The validate method can be used both as a classmethod (for stateless validators)
    or as an instance method (for validators that need initialization state).
    """

    def validate(self, result: CheckResult, args: argparse.Namespace) -> None:
        """
        Validate the given result. Can be called on both class and instance.
        Subclasses should implement this method.
        """
        raise NotImplementedError

