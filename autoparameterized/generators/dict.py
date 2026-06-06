"""Dictionary value generator."""

from ..base import TypeGenerator


class DictGenerator(TypeGenerator):
    """
    Generator for dictionary values with typed keys and values.

    Constraints:
        - size: Number of key-value pairs (default: 3)
        - key_type: Type of keys (default: str)
        - value_type: Type of values (default: str)
        - key_constraints: Constraints for key generator (dict)
        - value_constraints: Constraints for value generator (dict)
    """

    def __init__(self, constraints: dict = None, seed: int = None, resolver=None):
        super().__init__(constraints, seed)

        if resolver is None:
            from ..resolver import create_resolver
            resolver = create_resolver()
        self.resolver = resolver

    def generate(self) -> dict:
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

    def _seed_for(self, index: int, offset: int):
        if self.seed is None:
            return None
        return self.seed + index + offset
