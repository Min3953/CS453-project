"""Float value generator."""

import random

from ..base import TypeGenerator


class FloatGenerator(TypeGenerator):
    """
    Generator for floating-point values.

    Constraints:
        - min_value: Minimum value (default: 0.0)
        - max_value: Maximum value (default: 100.0)
    """

    def generate(self) -> float:
        if self.seed is not None:
            random.seed(self.seed)

        min_val = self.constraints.get('min_value', 0.0)
        max_val = self.constraints.get('max_value', 100.0)
        return random.uniform(min_val, max_val)
