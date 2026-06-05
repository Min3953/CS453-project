"""
Non-empty value customizer.
"""

from ..base import Customizer


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
