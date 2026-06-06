"""Dataclass value generator."""

import dataclasses
import typing

from ..base import TypeGenerator


class DataclassGenerator(TypeGenerator):
    """
    Generator for dataclass instances.

    The dataclass type is passed as a parameter, not in constraints.
    Type information is automatically extracted from the dataclass definition.

    Args:
        dataclass_type: The dataclass type to instantiate
        constraints: Field constraints (format: field__constraint=value)
        seed: Random seed for reproducibility
        resolver: Type resolver for nested types

    Constraints:
        - field_constraints: Per-field constraints keyed by field name
        - field_values: Explicit field values keyed by field name
        - Field constraints can also be provided as '<field>__<constraint>'

    Example:
        @dataclass
        class User:
            name: str
            age: int

        gen = DataclassGenerator(
            dataclass_type=User,
            constraints={'name__length': 5, 'age__min_value': 18},
            seed=42
        )
    """

    def __init__(self, dataclass_type, constraints: dict = None, seed: int = None, resolver=None):
        if not self._is_dataclass_type(dataclass_type):
            raise ValueError(f"{dataclass_type} must be a dataclass type")

        self.dataclass_type = dataclass_type
        super().__init__(constraints, seed)

        if resolver is None:
            from ..resolver import create_resolver
            resolver = create_resolver()
        self.resolver = resolver

    def generate(self):
        dataclass_type = self.dataclass_type

        field_values = self.constraints.get('field_values', {})
        type_hints = self._type_hints_for(dataclass_type)
        kwargs = {}

        for index, field in enumerate(dataclasses.fields(dataclass_type)):
            if not field.init:
                continue

            if field.name in field_values:
                kwargs[field.name] = field_values[field.name]
                continue

            field_type = type_hints.get(field.name, field.type)
            constraints = self._constraints_for_field(field.name)
            generator = self.resolver.resolve(
                field_type,
                constraints,
                self._seed_for(index),
            )
            kwargs[field.name] = generator.generate()

        return dataclass_type(**kwargs)

    def _constraints_for_field(self, field_name: str) -> dict:
        field_constraints = dict(
            self.constraints.get('field_constraints', {}).get(field_name, {})
        )
        prefix = f"{field_name}__"

        for key, value in self.constraints.items():
            if key.startswith(prefix):
                field_constraints[key[len(prefix):]] = value

        return field_constraints

    def _seed_for(self, index: int):
        if self.seed is None:
            return None
        return self.seed + index

    @staticmethod
    def _is_dataclass_type(value) -> bool:
        return isinstance(value, type) and dataclasses.is_dataclass(value)

    @staticmethod
    def _type_hints_for(dataclass_type) -> dict:
        try:
            return typing.get_type_hints(dataclass_type)
        except (NameError, TypeError):
            return {}
