"""
Composable customizer helper.
"""

from ..base import Customizer


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
