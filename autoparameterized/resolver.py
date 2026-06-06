"""
Type resolution implementation.

Provides registry-based type → generator mapping.
"""

import dataclasses
import typing
from datetime import datetime
from typing import Optional, Type

from .base import TypeGeneratorResolver, TypeGenerator


class RegistryBasedGeneratorResolver(TypeGeneratorResolver):
    """
    Registry-based implementation of type resolution.

    Maps types to generator classes using a simple dictionary.
    Supports:
        - Simple types (int, str, etc.)
        - Generic types (List[T], etc.) with recursive resolution
        - Custom generator registration
    """

    def __init__(self):
        """
        Initialize resolver with built-in generators.
        To customize, use register() method after initialization.
        """
        # Load built-in generators
        from .generators import (
            BoolGenerator,
            DateTimeGenerator,
            FloatGenerator,
            IntGenerator,
            StringGenerator,
        )

        self._generators = {
            bool: BoolGenerator,
            datetime: DateTimeGenerator,
            float: FloatGenerator,
            int: IntGenerator,
            str: StringGenerator,
        }

    def register(self, type_cls, generator_class: Type[TypeGenerator]):
        """
        Register a generator for a type.

        Args:
            type_cls: The type to register for
            generator_class: The generator class to use
        """
        self._generators[type_cls] = generator_class

    def resolve(self, param_type, constraints: dict = None, seed: Optional[int] = None) -> TypeGenerator:
        """
        Resolve a type to its generator instance.

        Priority:
        1. Generic types (List[T], etc.) - handled specially
        2. Registered types - simple lookup

        Args:
            param_type: The type to resolve
            constraints: Constraints for the generator
            seed: Random seed for reproducibility

        Returns:
            TypeGenerator instance

        Raises:
            ValueError: If no generator found for the type
        """
        constraints = constraints or {}

        # Check if it's a generic type (List[T], Optional[T], etc.)
        origin = typing.get_origin(param_type)

        if origin is list or param_type is list:
            # Handle List[T]
            return self._resolve_list(param_type, constraints, seed)

        if origin is dict or param_type is dict:
            # Handle Dict[K, V]
            return self._resolve_dict(param_type, constraints, seed)

        if self._is_dataclass_type(param_type):
            # Handle dataclass types
            return self._resolve_dataclass(param_type, constraints, seed)

        # Simple type lookup
        if param_type in self._generators:
            generator_class = self._generators[param_type]
            return generator_class(constraints=constraints, seed=seed)

        # No generator found
        raise ValueError(f"No generator registered for type: {param_type}")

    def _resolve_list(self, param_type, constraints: dict, seed: Optional[int]) -> TypeGenerator:
        """
        Resolve List[T] to ListGenerator.

        Args:
            param_type: The List[T] type
            constraints: Constraints including 'size' and element constraints
            seed: Random seed

        Returns:
            ListGenerator instance
        """
        # Lazy import to avoid circular dependency
        from .generators import ListGenerator

        args = typing.get_args(param_type)
        element_type = args[0] if args else str  # default to str

        # Build constraints for ListGenerator
        list_constraints = {
            'element_type': element_type,
            'size': constraints.get('size', 3),
        }

        # Extract element-specific constraints
        element_constraints = {k: v for k, v in constraints.items() if k not in ['size', 'element_type']}
        if element_constraints:
            list_constraints['element_constraints'] = element_constraints

        # Pass self as resolver so ListGenerator uses the same resolver instance
        return ListGenerator(constraints=list_constraints, seed=seed, resolver=self)

    def _resolve_dict(self, param_type, constraints: dict, seed: Optional[int]) -> TypeGenerator:
        """
        Resolve Dict[K, V] to DictGenerator.

        Args:
            param_type: The Dict[K, V] type
            constraints: Constraints including 'size' and key/value constraints
            seed: Random seed

        Returns:
            DictGenerator instance
        """
        # Lazy import to avoid circular dependency
        from .generators import DictGenerator

        args = typing.get_args(param_type)
        key_type = args[0] if args else str
        value_type = args[1] if len(args) > 1 else str

        dict_constraints = {
            'key_type': key_type,
            'value_type': value_type,
            'size': constraints.get('size', 3),
        }

        key_constraints = {
            key[len('key_'):]: value
            for key, value in constraints.items()
            if key.startswith('key_') and key != 'key_constraints'
        }
        value_constraints = {
            key[len('value_'):]: value
            for key, value in constraints.items()
            if key.startswith('value_') and key != 'value_constraints'
        }

        if 'key_constraints' in constraints:
            key_constraints.update(constraints['key_constraints'])
        if 'value_constraints' in constraints:
            value_constraints.update(constraints['value_constraints'])

        if key_constraints:
            dict_constraints['key_constraints'] = key_constraints
        if value_constraints:
            dict_constraints['value_constraints'] = value_constraints

        # Pass self as resolver so DictGenerator uses the same resolver instance
        return DictGenerator(constraints=dict_constraints, seed=seed, resolver=self)

    def _resolve_dataclass(self, param_type, constraints: dict, seed: Optional[int]) -> TypeGenerator:
        """
        Resolve a dataclass type to DataclassGenerator.

        Args:
            param_type: The dataclass type
            constraints: Field constraints
            seed: Random seed

        Returns:
            DataclassGenerator instance
        """
        # Lazy import to avoid circular dependency
        from .generators import DataclassGenerator

        dataclass_constraints = dict(constraints)
        dataclass_constraints['dataclass_type'] = param_type

        # Pass self as resolver so DataclassGenerator uses the same resolver instance
        return DataclassGenerator(
            constraints=dataclass_constraints,
            seed=seed,
            resolver=self,
        )

    @staticmethod
    def _is_dataclass_type(param_type) -> bool:
        return isinstance(param_type, type) and dataclasses.is_dataclass(param_type)


# ============================================================================
# Resolver factory function
# ============================================================================

def create_resolver() -> RegistryBasedGeneratorResolver:
    """
    Create a new resolver instance with default built-in generators.

    Returns a fresh resolver pre-registered with built-in generators
    (int, str, etc.).

    Each call creates a new independent instance, ensuring test isolation
    and avoiding global state issues.

    Returns:
        RegistryBasedGeneratorResolver instance
    """
    return RegistryBasedGeneratorResolver()
