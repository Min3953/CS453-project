"""
Demo implementations showing how to create generators.

These are example implementations to demonstrate the pattern.
Team members should create similar generators for other types.
"""

import random
import string
from .base import TypeGenerator, Customizer


# ============================================================================
# DEMO: Simple Generator
# ============================================================================

class IntGenerator(TypeGenerator):
    """
    Demo: Generator for integer values.

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


class StringGenerator(TypeGenerator):
    """
    Demo: Generator for string values.

    Constraints:
        - length: String length (default: 10)
        - charset: Character set to use (default: alphanumeric)
    """

    def generate(self) -> str:
        if self.seed is not None:
            random.seed(self.seed)

        length = self.constraints.get('length', 10)
        charset = self.constraints.get('charset', string.ascii_letters + string.digits)
        return ''.join(random.choices(charset, k=length))


# ============================================================================
# DEMO: Simple Customizer
# ============================================================================

class RangeCustomizer(Customizer):
    """
    Demo: Customizer that clamps numeric values to a range.
    """

    def __init__(self, min_value: float = None, max_value: float = None):
        self.min_value = min_value
        self.max_value = max_value

    def customize(self, value):
        if self.min_value is not None and value < self.min_value:
            return self.min_value
        if self.max_value is not None and value > self.max_value:
            return self.max_value
        return value


# ============================================================================
# TODO: Implement additional generators
# ============================================================================

# TODO: FloatGenerator - similar to IntGenerator but for floats
# TODO: BoolGenerator - random boolean values
# TODO: ListGenerator - generate lists of elements
# TODO: DictGenerator - generate dictionaries
# TODO: DateTimeGenerator - generate datetime objects
# TODO: DataclassGenerator - recursively generate dataclass instances

# ============================================================================
# TODO: Implement additional customizers
# ============================================================================

# TODO: LengthCustomizer - adjust string/list length
# TODO: TransformCustomizer - apply transformations (upper, lower, etc.)
# TODO: ChainCustomizer - compose multiple customizers
