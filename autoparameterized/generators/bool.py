"""Boolean value generator."""

import random

from ..base import TypeGenerator


class BoolGenerator(TypeGenerator):
    """
    Generator for boolean values.

    Constraints:
        - probability: Probability of generating True (default: 0.5)
    """

    def generate(self) -> bool:
        if self.seed is not None:
            random.seed(self.seed)

        probability = self.constraints.get('probability', 0.5)
        return random.random() < probability
