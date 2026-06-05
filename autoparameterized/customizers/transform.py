"""
Simple transformation value customizer.
"""

from ..base import Customizer


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
