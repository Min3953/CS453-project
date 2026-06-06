"""Literal value generator."""

import random

from ..base import TypeGenerator


class LiteralGenerator(TypeGenerator):
    """
    Generator for typing.Literal values.

    Args:
        choices: Literal values to choose from
        constraints: Additional constraints
        seed: Random seed for reproducibility

    Constraints:
        - choices: Optional override for literal choices
    """

    def __init__(self, choices=None, constraints: dict = None, seed: int = None):
        self.choices = tuple(choices or ())
        super().__init__(constraints, seed)

    def generate(self):
        if self.seed is not None:
            random.seed(self.seed)

        choices = tuple(self.constraints.get('choices', self.choices))
        if not choices:
            raise ValueError("choices must contain at least one literal value")

        return random.choice(choices)
