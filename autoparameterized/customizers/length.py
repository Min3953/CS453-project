"""
Length-based value customizer.
"""

from ..base import Customizer


class LengthCustomizer(Customizer):
    """
    Customizer that adjusts string/list values to a requested length.
    """

    def __init__(self, length=None, min_length=None, max_length=None, fill_value=None):
        for name, value in (
            ("length", length),
            ("min_length", min_length),
            ("max_length", max_length),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{name} must be non-negative")

        if min_length is not None and max_length is not None and min_length > max_length:
            raise ValueError("min_length must be less than or equal to max_length")

        self.length = length
        self.min_length = min_length
        self.max_length = max_length
        self.fill_value = fill_value

    def customize(self, value):
        if not isinstance(value, (str, list)):
            return value

        target_length = None

        if self.length is not None:
            target_length = self.length
        elif self.max_length is not None and len(value) > self.max_length:
            target_length = self.max_length
        elif self.min_length is not None and len(value) < self.min_length:
            target_length = self.min_length

        if target_length is None or len(value) == target_length:
            return value

        if len(value) > target_length:
            return value[:target_length]

        missing = target_length - len(value)

        if isinstance(value, str):
            fill_text = " " if self.fill_value is None else str(self.fill_value)
            if fill_text == "":
                fill_text = " "
            return value + (fill_text * missing)[:missing]

        return value + [self.fill_value] * missing
