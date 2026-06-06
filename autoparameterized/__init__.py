"""
autoparameterized - Type-hint based automatic test parameterization

This is a skeleton package for team development.
Core interfaces are defined, implementation is split among team members.
"""

# Base interfaces (COMPLETE)
from .base import TypeGenerator, Customizer

# Demo implementations (REFERENCE ONLY)
from .generators import (
    BoolGenerator,
    DateTimeGenerator,
    DictGenerator,
    FloatGenerator,
    IntGenerator,
    StringGenerator,
    RangeCustomizer,
)

# Core decorator (SKELETON - TO BE COMPLETED)
from .decorator import (
    autosource,
    register_generator,
    with_customizer,
    freeze_param,
)

__version__ = "0.1.0-dev"
__all__ = [
    # Base interfaces
    "TypeGenerator",
    "Customizer",
    # Demo implementations
    "BoolGenerator",
    "DateTimeGenerator",
    "DictGenerator",
    "FloatGenerator",
    "IntGenerator",
    "StringGenerator",
    "RangeCustomizer",
    # Decorators
    "autosource",
    "register_generator",
    "with_customizer",
    "freeze_param",
]
