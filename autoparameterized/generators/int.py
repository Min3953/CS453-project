"""Integer value generator."""

import random

from ..base import TypeGenerator


class IntGenerator(TypeGenerator):
    """
    Generator for integer values.

    Constraints:
        - min_value: Minimum value (default: 0)
        - max_value: Maximum value (default: 100)
    """

    def generate(self) -> int:
        if self.seed is not None:
            random.seed(self.seed)

        min_val = self.constraints.get('min_value', 0)
        max_val = self.constraints.get('max_value', 100)
        return random.randint(min_val, max_val)
