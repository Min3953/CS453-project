"""Enum value generator."""

import enum
import random

from ..base import TypeGenerator


class EnumGenerator(TypeGenerator):
    """
    Generator for enum values.

    Args:
        enum_type: Enum class to generate values from
        constraints: Additional constraints
        seed: Random seed for reproducibility

    Constraints:
        - choices: Optional subset of enum members to choose from
    """

    def __init__(self, enum_type, constraints: dict = None, seed: int = None):
        if not self._is_enum_type(enum_type):
            raise ValueError(f"{enum_type} must be an Enum type")

        self.enum_type = enum_type
        super().__init__(constraints, seed)

    def generate(self):
        if self.seed is not None:
            random.seed(self.seed)

        choices = tuple(self.constraints.get('choices', tuple(self.enum_type)))
        if not choices:
            raise ValueError("choices must contain at least one enum member")

        return random.choice(choices)

    @staticmethod
    def _is_enum_type(value) -> bool:
        return isinstance(value, type) and issubclass(value, enum.Enum)
