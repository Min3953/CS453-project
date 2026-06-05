"""
Reusable value customizers for generated test inputs.
"""

from ..base import Customizer
from .chain import ChainCustomizer
from .length import LengthCustomizer
from .regex_string import RegexStringCustomizer
from .transform import TransformCustomizer


class TypeCastCustomizer(Customizer):
    """
    Customizer that casts values to a target type.
    """

    def __init__(self, target_type, fallback=None):
        allowed_types = (int, str, float)

        if target_type not in allowed_types:
            raise TypeError("target_type must be int, str, or float")

        self.target_type = target_type
        self.fallback = fallback

    def customize(self, value):
        try:
            return self.target_type(value)
        except (TypeError, ValueError):
            if self.fallback is not None:
                return self.fallback
            return value


class NonEmptyCustomizer(Customizer):
    """
    Customizer that replaces empty strings/lists with defaults.
    """

    def __init__(self, default_string="value", default_item=None):
        self.default_string = default_string
        self.default_item = default_item

    def customize(self, value):
        if isinstance(value, str) and value == "":
            return self.default_string

        if isinstance(value, list) and len(value) == 0:
            return [self.default_item]

        return value


__all__ = [
    "LengthCustomizer",
    "TransformCustomizer",
    "ChainCustomizer",
    "RegexStringCustomizer",
    "TypeCastCustomizer",
    "NonEmptyCustomizer",
]
