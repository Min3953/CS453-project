"""
Reusable value customizers for generated test inputs.
"""

import re

from .base import Customizer


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


class TransformCustomizer(Customizer):
    """
    Customizer that applies a simple transformation to a value.
    """

    def __init__(self, transform):
        allowed_transforms = ("upper", "lower", "strip", "title")

        if isinstance(transform, str) and transform not in allowed_transforms:
            raise ValueError(f"Unknown transform: {transform}")

        if not isinstance(transform, str) and not callable(transform):
            raise TypeError("transform must be a string or callable")

        self.transform = transform

    def customize(self, value):
        if callable(self.transform):
            return self.transform(value)

        if not hasattr(value, self.transform):
            return value

        transform = getattr(value, self.transform)
        if not callable(transform):
            return value

        return transform()


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
