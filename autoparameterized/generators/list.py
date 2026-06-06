"""List value generator."""

import typing

from ..base import TypeGenerator


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
            from ..resolver import create_resolver
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
