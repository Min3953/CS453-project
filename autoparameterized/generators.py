"""
Demo implementations showing how to create generators.

These are example implementations to demonstrate the pattern.
Team members should create similar generators for other types.
"""

import random
import string
import typing

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


class ListGenerator(TypeGenerator):
    """
    Generator for list values with typed elements.

    Delegates element generation to the appropriate type generator
    via a TypeGeneratorResolver.

    Constraints:
        - size: Number of elements (default: 3)
        - element_type: Type of elements (default: str)
        - element_constraints: Constraints for element generator (dict)
    """

    def __init__(self, constraints: dict = None, seed: int = None, resolver=None):
        """
        Initialize ListGenerator.

        Args:
            constraints: Constraints dict
            seed: Random seed
            resolver: TypeGeneratorResolver instance (creates new one if None)
        """
        super().__init__(constraints, seed)

        # Use provided resolver or create a new one
        if resolver is None:
            from .resolver import create_resolver
            resolver = create_resolver()
        self.resolver = resolver

    def generate(self) -> typing.List:
        """
        Generate a list of elements by delegating to resolver.

        Returns:
            List of generated values
        """
        size = self.constraints.get('size', 3)
        element_type = self.constraints.get('element_type', str)  # default to str
        element_constraints = self.constraints.get('element_constraints', {})

        # Use resolver to get generator for element type
        gen = self.resolver.resolve(element_type, element_constraints, self.seed)

        return [gen.generate() for _ in range(size)]


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
# TODO: DictGenerator - generate dictionaries
# TODO: DateTimeGenerator - generate datetime objects
# TODO: DataclassGenerator - recursively generate dataclass instances

# ============================================================================
# TODO: Implement additional customizers
# ============================================================================

# TODO: LengthCustomizer - adjust string/list length
# TODO: TransformCustomizer - apply transformations (upper, lower, etc.)
# TODO: ChainCustomizer - compose multiple customizers
