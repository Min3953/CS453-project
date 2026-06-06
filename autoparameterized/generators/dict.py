"""Dictionary value generator."""

import sys
import typing

from ..base import TypeGenerator


class DictGenerator(TypeGenerator):
    """
    Generator for dictionary values with flexible schema support.

    Three modes of operation:

    1. Schema mode - Define exact keys and types:
        DictGenerator(
            schema={
                'name': {'type': str, 'length': 5},
                'age': {'type': int, 'min_value': 18},
            },
            seed=42
        )

    2. TypedDict mode - Automatically extract schema from TypedDict:
        DictGenerator(
            typed_dict=MyTypedDict,
            constraints={'name__length': 5},
            seed=42
        )

    3. Dynamic mode (legacy) - All keys/values same type:
        DictGenerator(
            constraints={'size': 3, 'key_type': str, 'value_type': int},
            seed=42
        )

    Args:
        typed_dict: TypedDict class (for TypedDict mode)
        schema: Schema dict (for Schema mode)
        constraints: Additional constraints
        seed: Random seed
        resolver: Type resolver

    Constraints:
        Schema mode:
            - Field constraints use format: key__constraint=value

        TypedDict mode:
            - Field constraints use format: key__constraint=value

        Dynamic mode:
            - size: Number of key-value pairs (default: 3)
            - key_type: Type of keys (default: str)
            - value_type: Type of values (default: str)
            - key_constraints: Constraints for key generator
            - value_constraints: Constraints for value generator
    """

    def __init__(
        self,
        typed_dict=None,
        schema=None,
        constraints: dict = None,
        seed: int = None,
        resolver=None
    ):
        self.typed_dict = typed_dict
        self.schema = schema
        super().__init__(constraints, seed)

        if resolver is None:
            from ..resolver import create_resolver
            resolver = create_resolver()
        self.resolver = resolver

    def generate(self) -> dict:
        # Check if schema mode
        if self.schema:
            return self._generate_from_schema(self.schema)

        # Check if TypedDict mode
        if self.typed_dict and self._is_typed_dict(self.typed_dict):
            return self._generate_from_typed_dict(self.typed_dict)

        # Default to dynamic mode (legacy)
        return self._generate_dynamic()

    def _generate_from_schema(self, schema: dict) -> dict:
        """Generate dict from explicit schema definition."""
        result = {}

        for index, (key, spec) in enumerate(schema.items()):
            # Parse spec: can be a type or a dict with 'type' and constraints
            if isinstance(spec, dict):
                value_type = spec.get('type', str)
                # Extract constraints for this field
                field_constraints = {k: v for k, v in spec.items() if k != 'type'}
            else:
                # Spec is just a type
                value_type = spec
                field_constraints = {}

            # Also check for field__constraint style constraints
            field_constraints.update(self._constraints_for_field(key))

            # Generate value
            generator = self.resolver.resolve(
                value_type,
                field_constraints,
                self._seed_for(index),
            )
            result[key] = generator.generate()

        return result

    def _generate_from_typed_dict(self, typed_dict_class) -> dict:
        """Generate dict from TypedDict class."""
        # Extract type hints from TypedDict
        try:
            type_hints = typing.get_type_hints(typed_dict_class)
        except (NameError, TypeError):
            type_hints = {}

        result = {}

        for index, (key, value_type) in enumerate(type_hints.items()):
            # Get constraints for this field
            field_constraints = self._constraints_for_field(key)

            # Generate value
            generator = self.resolver.resolve(
                value_type,
                field_constraints,
                self._seed_for(index),
            )
            result[key] = generator.generate()

        return result

    def _generate_dynamic(self) -> dict:
        """Generate dict with dynamic keys (legacy mode)."""
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

    def _constraints_for_field(self, field_name: str) -> dict:
        """Extract field-specific constraints from param__constraint format."""
        field_constraints = {}
        prefix = f"{field_name}__"

        for key, value in self.constraints.items():
            if key.startswith(prefix):
                constraint_name = key[len(prefix):]
                field_constraints[constraint_name] = value

        return field_constraints

    def _seed_for(self, index: int, offset: int = 0):
        """Generate seed for the nth field."""
        if self.seed is None:
            return None
        return self.seed + index + offset

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
