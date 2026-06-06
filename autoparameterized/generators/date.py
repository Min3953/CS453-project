"""Date value generator."""

import random
from datetime import date, timedelta

from ..base import TypeGenerator


class DateGenerator(TypeGenerator):
    """
    Generator for date values.

    Constraints:
        - min_value: Earliest date (default: 1970-01-01)
        - max_value: Latest date (default: 2030-12-31)
        - start: Alias for min_value
        - end: Alias for max_value
    """

    DEFAULT_START = date(1970, 1, 1)
    DEFAULT_END = date(2030, 12, 31)

    def generate(self) -> date:
        if self.seed is not None:
            random.seed(self.seed)

        start = self.constraints.get(
            'min_value',
            self.constraints.get('start', self.DEFAULT_START),
        )
        end = self.constraints.get(
            'max_value',
            self.constraints.get('end', self.DEFAULT_END),
        )

        if end < start:
            raise ValueError("max_value must be greater than or equal to min_value")

        span_days = (end - start).days
        offset_days = random.randint(0, span_days)
        return start + timedelta(days=offset_days)
