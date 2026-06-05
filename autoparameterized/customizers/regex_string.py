"""
Regex-based string customizer.
"""

import re

from ..base import Customizer


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
