"""Dataclass value generator."""

import dataclasses
import typing

from ..base import TypeGenerator


class DataclassGenerator(TypeGenerator):
    """
    Generator for dataclass instances.

    Constraints:
        - dataclass_type: Dataclass type to instantiate
        - field_constraints: Per-field constraints keyed by field name
        - field_values: Explicit field values keyed by field name

    Field constraints can also be provided as '<field>__<constraint>'.
    """

    def __init__(self, constraints: dict = None, seed: int = None, resolver=None):
        super().__init__(constraints, seed)

        if resolver is None:
            from ..resolver import create_resolver
            resolver = create_resolver()
        self.resolver = resolver

    def generate(self):
        dataclass_type = self.constraints.get(
            'dataclass_type',
            self.constraints.get('target_type'),
        )
        if not self._is_dataclass_type(dataclass_type):
            raise ValueError("dataclass_type must be a dataclass type")

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
