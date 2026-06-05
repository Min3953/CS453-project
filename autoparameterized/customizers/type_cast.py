"""
Type casting value customizer.
"""

from ..base import Customizer


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
