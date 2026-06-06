"""DateTime value generator."""

import random
from datetime import datetime, timedelta

from ..base import TypeGenerator


class DateTimeGenerator(TypeGenerator):
    """
    Generator for datetime values.

    Constraints:
        - min_value: Earliest datetime (default: 1970-01-01 00:00:00)
        - max_value: Latest datetime (default: 2030-12-31 23:59:59)
        - start: Alias for min_value
        - end: Alias for max_value
    """

    DEFAULT_START = datetime(1970, 1, 1)
    DEFAULT_END = datetime(2030, 12, 31, 23, 59, 59)

    def generate(self) -> datetime:
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

        span_seconds = (end - start).total_seconds()
        offset_seconds = random.uniform(0, span_seconds)
        return start + timedelta(seconds=offset_seconds)
