"""Tuple value generator."""

import typing

from ..base import TypeGenerator


class TupleGenerator(TypeGenerator):
    """
    Generator for tuple values with typed elements.

    Supports both homogeneous tuples (Tuple[T, ...]) and fixed-shape tuples
    (Tuple[T1, T2, ...]).

    Constraints:
        - size: Number of elements for homogeneous tuples (default: 3)
        - element_type: Type for homogeneous tuple elements (default: str)
        - element_types: Types for fixed-shape tuple elements
        - element_constraints: Constraints applied to every element
        - index_constraints: Per-index constraints keyed by index
        - <index>__<constraint>: Per-index constraint shorthand
    """

    def __init__(self, constraints: dict = None, seed: int = None, resolver=None):
        """
        Initialize TupleGenerator.

        Args:
            constraints: Constraints dict
            seed: Random seed
            resolver: TypeGeneratorResolver instance (creates new one if None)
        """
        super().__init__(constraints, seed)

        if resolver is None:
            from ..resolver import create_resolver
            resolver = create_resolver()
        self.resolver = resolver

    def generate(self) -> typing.Tuple:
        """
        Generate a tuple of elements by delegating to resolver.

        Returns:
            Tuple of generated values
        """
        element_types = self.constraints.get('element_types')

        if element_types is not None:
            return tuple(
                self._generate_element(index, element_type)
                for index, element_type in enumerate(element_types)
            )

        size = self.constraints.get('size', 3)
        element_type = self.constraints.get('element_type', str)

        return tuple(
            self._generate_element(index, element_type)
            for index in range(size)
        )

    def _generate_element(self, index: int, element_type):
        generator = self.resolver.resolve(
            element_type,
            self._constraints_for_index(index),
            self._seed_for(index),
        )
        return generator.generate()

    def _constraints_for_index(self, index: int) -> dict:
        constraints = dict(self.constraints.get('element_constraints', {}))
        index_constraints = self.constraints.get('index_constraints', {})

        constraints.update(index_constraints.get(index, {}))
        constraints.update(index_constraints.get(str(index), {}))

        prefix = f"{index}__"
        for key, value in self.constraints.items():
            if key.startswith(prefix):
                constraints[key[len(prefix):]] = value

        return constraints

    def _seed_for(self, index: int):
        if self.seed is None:
            return None
        return self.seed + index
