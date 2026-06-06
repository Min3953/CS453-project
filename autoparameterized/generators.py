"""
Demo implementations showing how to create generators.

These are example implementations to demonstrate the pattern.
Team members should create similar generators for other types.
"""

import random
import string
import typing
from datetime import datetime, timedelta

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


class BoolGenerator(TypeGenerator):
    """
    Generator for boolean values.

    Constraints:
        - probability: Probability of generating True (default: 0.5)
    """

    def generate(self) -> bool:
        if self.seed is not None:
            random.seed(self.seed)

        probability = self.constraints.get('probability', 0.5)
        return random.random() < probability


class DictGenerator(TypeGenerator):
    """
    Generator for dictionary values with typed keys and values.

    Constraints:
        - size: Number of key-value pairs (default: 3)
        - key_type: Type of keys (default: str)
        - value_type: Type of values (default: str)
        - key_constraints: Constraints for key generator (dict)
        - value_constraints: Constraints for value generator (dict)
    """

    def __init__(self, constraints: dict = None, seed: int = None, resolver=None):
        super().__init__(constraints, seed)

        if resolver is None:
            from .resolver import create_resolver
            resolver = create_resolver()
        self.resolver = resolver

    def generate(self) -> dict:
        size = self.constraints.get('size', 3)
        key_type = self.constraints.get('key_type', str)
        value_type = self.constraints.get('value_type', str)
        key_constraints = self.constraints.get('key_constraints', {})
        value_constraints = self.constraints.get('value_constraints', {})
        max_attempts = self.constraints.get('max_attempts', max(size * 10, 10))

        result = {}
        attempts = 0

        while len(result) < size:
            if attempts >= max_attempts:
                raise ValueError("could not generate enough unique dictionary keys")

            key_generator = self.resolver.resolve(
                key_type,
                key_constraints,
                self._seed_for(attempts, 0),
            )
            value_generator = self.resolver.resolve(
                value_type,
                value_constraints,
                self._seed_for(attempts, max_attempts),
            )

            key = key_generator.generate()
            try:
                already_present = key in result
            except TypeError as exc:
                raise ValueError("generated dictionary keys must be hashable") from exc

            if not already_present:
                result[key] = value_generator.generate()

            attempts += 1

        return result

    def _seed_for(self, index: int, offset: int):
        if self.seed is None:
            return None
        return self.seed + index + offset


class DateTimeGenerator(TypeGenerator):
    """
    Generator for datetime values.

    Constraints:
        - min_value: Earliest datetime (default: 1970-01-01 00:00:00)
        - max_value: Latest datetime (default: 2030-12-31 23:59:59)
        - start: Alias for min_value
        - end: Alias for max_value
    """

    DEFAULT_START = datetime(1970, 1, 1)
    DEFAULT_END = datetime(2030, 12, 31, 23, 59, 59)

    def generate(self) -> datetime:
        if self.seed is not None:
            random.seed(self.seed)

        start = self.constraints.get(
            'min_value',
            self.constraints.get('start', self.DEFAULT_START),
        )
        end = self.constraints.get(
            'max_value',
            self.constraints.get('end', self.DEFAULT_END),
        )

        if end < start:
            raise ValueError("max_value must be greater than or equal to min_value")

        span_seconds = (end - start).total_seconds()
        offset_seconds = random.uniform(0, span_seconds)
        return start + timedelta(seconds=offset_seconds)


# TODO: DataclassGenerator - recursively generate dataclass instances

# ============================================================================
# TODO: Implement additional customizers
# ============================================================================

# TODO: LengthCustomizer - adjust string/list length
# TODO: TransformCustomizer - apply transformations (upper, lower, etc.)
# TODO: ChainCustomizer - compose multiple customizers
