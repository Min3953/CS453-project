"""
Type resolution implementation.

Provides registry-based type → generator mapping.
"""

import dataclasses
import enum
import sys
import typing
from datetime import date, datetime
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
            DateGenerator,
            DateTimeGenerator,
            FloatGenerator,
            IntGenerator,
            StringGenerator,
        )

        self._generators = {
            bool: BoolGenerator,
            date: DateGenerator,
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

        if origin is set or param_type is set:
            # Handle Set[T]
            return self._resolve_set(param_type, constraints, seed)

        if origin is dict or param_type is dict:
            # Handle Dict[K, V]
            return self._resolve_dict(param_type, constraints, seed)

        if origin is tuple or param_type is tuple:
            # Handle Tuple[T, ...] and Tuple[T1, T2, ...]
            return self._resolve_tuple(param_type, constraints, seed)

        if origin is typing.Literal:
            # Handle Literal[...] finite choices
            return self._resolve_literal(param_type, constraints, seed)

        if self._is_typed_dict(param_type):
            # Handle TypedDict types
            return self._resolve_typed_dict(param_type, constraints, seed)

        if self._is_enum_type(param_type):
            # Handle Enum subclasses
            return self._resolve_enum(param_type, constraints, seed)

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

    def _resolve_set(self, param_type, constraints: dict, seed: Optional[int]) -> TypeGenerator:
        """
        Resolve Set[T] to SetGenerator.

        Args:
            param_type: The Set[T] type
            constraints: Constraints including 'size' and element constraints
            seed: Random seed

        Returns:
            SetGenerator instance
        """
        # Lazy import to avoid circular dependency
        from .generators import SetGenerator

        args = typing.get_args(param_type)
        element_type = args[0] if args else str  # default to str

        # Build constraints for SetGenerator
        set_constraints = {
            'element_type': element_type,
            'size': constraints.get('size', 3),
        }

        # Extract element-specific constraints
        element_constraints = {k: v for k, v in constraints.items() if k not in ['size', 'element_type']}
        if element_constraints:
            set_constraints['element_constraints'] = element_constraints

        # Pass self as resolver so SetGenerator uses the same resolver instance
        return SetGenerator(constraints=set_constraints, seed=seed, resolver=self)

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

    def _resolve_tuple(self, param_type, constraints: dict, seed: Optional[int]) -> TypeGenerator:
        """
        Resolve Tuple[T, ...] or Tuple[T1, T2, ...] to TupleGenerator.

        Args:
            param_type: The Tuple type
            constraints: Constraints including 'size' and element/index constraints
            seed: Random seed

        Returns:
            TupleGenerator instance
        """
        from .generators import TupleGenerator

        args = typing.get_args(param_type)
        tuple_constraints = {}

        if args and not self._is_homogeneous_tuple_args(args):
            tuple_constraints['element_types'] = args
        else:
            element_type = args[0] if args else str
            tuple_constraints.update({
                'element_type': element_type,
                'size': constraints.get('size', 3),
            })

        if 'index_constraints' in constraints:
            tuple_constraints['index_constraints'] = constraints['index_constraints']

        element_constraints = dict(constraints.get('element_constraints', {}))
        for key, value in constraints.items():
            if key in {'size', 'element_type', 'element_types', 'element_constraints', 'index_constraints'}:
                continue

            if self._is_tuple_index_constraint(key):
                tuple_constraints[key] = value
            else:
                element_constraints[key] = value

        if element_constraints:
            tuple_constraints['element_constraints'] = element_constraints

        return TupleGenerator(constraints=tuple_constraints, seed=seed, resolver=self)

    def _resolve_literal(self, param_type, constraints: dict, seed: Optional[int]) -> TypeGenerator:
        """
        Resolve Literal[...] to LiteralGenerator.

        Args:
            param_type: The Literal type
            constraints: Constraints for the generator
            seed: Random seed

        Returns:
            LiteralGenerator instance
        """
        from .generators import LiteralGenerator

        return LiteralGenerator(
            choices=typing.get_args(param_type),
            constraints=constraints,
            seed=seed,
        )

    def _resolve_enum(self, param_type, constraints: dict, seed: Optional[int]) -> TypeGenerator:
        """
        Resolve an Enum subclass to EnumGenerator.

        Args:
            param_type: The Enum subclass
            constraints: Constraints for the generator
            seed: Random seed

        Returns:
            EnumGenerator instance
        """
        from .generators import EnumGenerator

        return EnumGenerator(
            enum_type=param_type,
            constraints=constraints,
            seed=seed,
        )

    def _resolve_typed_dict(self, param_type, constraints: dict, seed: Optional[int]) -> TypeGenerator:
        """
        Resolve a TypedDict type to DictGenerator.

        Args:
            param_type: The TypedDict type
            constraints: Field constraints
            seed: Random seed

        Returns:
            DictGenerator instance
        """
        # Lazy import to avoid circular dependency
        from .generators import DictGenerator

        # Pass typed_dict directly, not through constraints
        return DictGenerator(
            typed_dict=param_type,
            constraints=constraints,
            seed=seed,
            resolver=self,
        )

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

        # Pass dataclass_type directly, not through constraints
        return DataclassGenerator(
            dataclass_type=param_type,
            constraints=constraints,
            seed=seed,
            resolver=self,
        )

    @staticmethod
    def _is_typed_dict(cls) -> bool:
        """Check if a class is a TypedDict."""
        # Python 3.10+: typing.is_typeddict()
        if sys.version_info >= (3, 10):
            return typing.is_typeddict(cls)

        # Python 3.8-3.9: Check for __annotations__ and __total__
        return (
            isinstance(cls, type)
            and hasattr(cls, '__annotations__')
            and hasattr(cls, '__total__')
        )

    @staticmethod
    def _is_dataclass_type(param_type) -> bool:
        return isinstance(param_type, type) and dataclasses.is_dataclass(param_type)

    @staticmethod
    def _is_enum_type(param_type) -> bool:
        return isinstance(param_type, type) and issubclass(param_type, enum.Enum)

    @staticmethod
    def _is_homogeneous_tuple_args(args) -> bool:
        return len(args) == 2 and args[1] is Ellipsis

    @staticmethod
    def _is_tuple_index_constraint(key: str) -> bool:
        index, separator, _ = key.partition('__')
        return bool(separator) and index.isdigit()


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
