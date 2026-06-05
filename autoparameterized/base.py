"""
Base interfaces for type-hint based automatic parameterization.

This module defines the core contracts that all components must follow.
"""

from typing import Any, Optional, Type


class TypeGenerator:
    """
    Base interface for type-specific value generators.

    Each generator is responsible for creating random/test values
    for a specific Python type.

    Contract:
        - Accept constraints dict and optional seed in __init__
        - Implement generate() to return a value of the target type
        - Use self.seed for reproducible random generation

    Example implementation:
        class IntGenerator(TypeGenerator):
            def generate(self) -> int:
                min_val = self.constraints.get('min_value', 0)
                max_val = self.constraints.get('max_value', 100)
                return random.randint(min_val, max_val)
    """

    def __init__(self, constraints: dict = None, seed: Optional[int] = None):
        """
        Initialize the generator.

        Args:
            constraints: Dictionary of constraints (e.g., {'min_value': 0, 'max_value': 100})
            seed: Random seed for reproducible generation
        """
        self.constraints = constraints or {}
        self.seed = seed

    def generate(self) -> Any:
        """
        Generate a value of the target type.

        Returns:
            A generated value

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement generate()")


class Customizer:
    """
    Base interface for value customization/transformation.

    Customizers are applied after generation to transform or
    constrain values (e.g., clamping to range, converting case).

    Contract:
        - Implement customize() to transform a value
        - Should be idempotent when possible
        - Should not raise exceptions on invalid input

    Example implementation:
        class RangeCustomizer(Customizer):
            def __init__(self, min_value, max_value):
                self.min_value = min_value
                self.max_value = max_value

            def customize(self, value):
                return max(self.min_value, min(self.max_value, value))
    """

    def customize(self, value: Any) -> Any:
        """
        Transform a generated value.

        Args:
            value: The value to customize

        Returns:
            The transformed value
        """
        return value


class TypeGeneratorResolver:
    """
    Interface for resolving types to their appropriate generators.

    Implementations handle the mapping from Python types (int, str, List[T], etc.)
    to generator instances that can produce values of those types.

    Used by:
        - @autosource decorator
        - Recursive generators (ListGenerator, DictGenerator, etc.)
    """

    def resolve(self, param_type, constraints: dict = None, seed: Optional[int] = None) -> TypeGenerator:
        """
        Resolve a type to its generator instance.

        Args:
            param_type: The type to resolve (e.g., int, str, List[int])
            constraints: Optional constraints for the generator
            seed: Optional random seed for reproducibility

        Returns:
            TypeGenerator instance capable of generating values of param_type

        Raises:
            ValueError: If no generator can be found for the type
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement resolve()")

    def register(self, type_cls, generator_class: Type[TypeGenerator]):
        """
        Register a custom generator for a type.

        Args:
            type_cls: The type to register for
            generator_class: The generator class to use

        Note:
            Not all implementations may support registration.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement register()")
