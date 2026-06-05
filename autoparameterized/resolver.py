"""
Type resolution implementation.

Provides registry-based type → generator mapping.
"""

import typing
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
        from .generators import IntGenerator, StringGenerator

        self._generators = {
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
        pass

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

        if origin is list:
            # Handle List[T]
            return self._resolve_list(param_type, constraints, seed)

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
        element_constraints = {k: v for k, v in constraints.items() if k not in ['size']}
        if element_constraints:
            list_constraints['element_constraints'] = element_constraints

        # Pass self as resolver so ListGenerator uses the same resolver instance
        return ListGenerator(constraints=list_constraints, seed=seed, resolver=self)


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
