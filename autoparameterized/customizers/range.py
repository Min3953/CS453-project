"""
Range customizer for clamping numeric values.
"""

from ..base import Customizer


class RangeCustomizer(Customizer):
    """
    Customizer that clamps numeric values to a range.

    Args:
        min_value: Minimum allowed value (None for no lower bound)
        max_value: Maximum allowed value (None for no upper bound)
    """

    def __init__(self, min_value: float = None, max_value: float = None):
        self.min_value = min_value
        self.max_value = max_value

    def customize(self, value):
        """
        Clamp value to the specified range.

        Args:
            value: Value to clamp

        Returns:
            Clamped value
        """
        if self.min_value is not None and value < self.min_value:
            return self.min_value
        if self.max_value is not None and value > self.max_value:
            return self.max_value
        return value
