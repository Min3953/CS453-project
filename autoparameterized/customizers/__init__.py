"""
Reusable value customizers for generated test inputs.
"""

import re

from ..base import Customizer
from .length import LengthCustomizer
from .transform import TransformCustomizer


class ChainCustomizer(Customizer):
    """
    Customizer that composes multiple customizers in order.
    """

    def __init__(self, *customizers):
        for customizer in customizers:
            customize = getattr(customizer, "customize", None)
            if not callable(customize):
                raise TypeError("customizers must have a customize method")

        self.customizers = customizers

    def customize(self, value):
        for customizer in self.customizers:
            value = customizer.customize(value)
        return value


class RegexStringCustomizer(Customizer):
    """
    Customizer that keeps strings matching a regex pattern.
    """

    def __init__(self, pattern, fallback=""):
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")

        if not isinstance(fallback, str):
            raise TypeError("fallback must be a string")

        try:
            self.pattern = re.compile(pattern)
        except re.error as error:
            raise ValueError(f"Invalid regex pattern: {pattern}") from error

        if not self.pattern.fullmatch(fallback):
            raise ValueError("fallback must match the pattern")

        self.fallback = fallback

    def customize(self, value):
        if not isinstance(value, str):
            return value

        if self.pattern.fullmatch(value):
            return value

        return self.fallback


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
