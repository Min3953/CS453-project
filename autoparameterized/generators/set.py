"""Set value generator."""

import typing

from ..base import TypeGenerator


class SetGenerator(TypeGenerator):
    """
    Generator for set values with typed elements.

    Delegates element generation to the appropriate type generator
    via a TypeGeneratorResolver. Ensures all elements are unique.

    Constraints:
        - size: Number of elements (default: 3)
        - element_type: Type of elements (default: str)
        - element_constraints: Constraints for element generator (dict)
    """

    def __init__(self, constraints: dict = None, seed: int = None, resolver=None):
        """
        Initialize SetGenerator.

        Args:
            constraints: Constraints dict
            seed: Random seed
            resolver: TypeGeneratorResolver instance (creates new one if None)
        """
        super().__init__(constraints, seed)

        # Use provided resolver or create a new one
        if resolver is None:
            from ..resolver import create_resolver
            resolver = create_resolver()
        self.resolver = resolver

    def generate(self) -> typing.Set:
        """
        Generate a set of unique elements by delegating to resolver.

        Returns:
            Set of generated values
        """
        size = self.constraints.get('size', 3)
        element_type = self.constraints.get('element_type', str)  # default to str
        element_constraints = self.constraints.get('element_constraints', {})

        result = set()
        attempts = 0

        while len(result) < size:
            # Use different seed for each attempt to get different values
            effective_seed = self._seed_for(attempts) if self.seed is not None else None
            gen = self.resolver.resolve(element_type, element_constraints, effective_seed)

            try:
                element = gen.generate()
                result.add(element)
            except TypeError as exc:
                raise ValueError("Set elements must be hashable") from exc

            attempts += 1

        return result

    def _seed_for(self, index: int):
        """Generate a seed for the nth element."""
        if self.seed is None:
            return None
        return self.seed + index
