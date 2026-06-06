"""
autoparameterized - Type-hint based automatic test parameterization

This is a skeleton package for team development.
Core interfaces are defined, implementation is split among team members.
"""

# Base interfaces (COMPLETE)
from .base import TypeGenerator, Customizer

from .generators import (
    BoolGenerator,
    DateGenerator,
    DataclassGenerator,
    DateTimeGenerator,
    DictGenerator,
    EnumGenerator,
    FloatGenerator,
    IntGenerator,
    LiteralGenerator,
    StringGenerator,
    TupleGenerator,
)

from .customizers import (
    ChainCustomizer,
    LengthCustomizer,
    NonEmptyCustomizer,
    RangeCustomizer,
    RegexStringCustomizer,
    TransformCustomizer,
    TypeCastCustomizer,
)

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
    "BoolGenerator",
    "DateGenerator",
    "DataclassGenerator",
    "DateTimeGenerator",
    "DictGenerator",
    "EnumGenerator",
    "FloatGenerator",
    "IntGenerator",
    "LiteralGenerator",
    "StringGenerator",
    "TupleGenerator",
    # Customizers
    "ChainCustomizer",
    "LengthCustomizer",
    "NonEmptyCustomizer",
    "RangeCustomizer",
    "RegexStringCustomizer",
    "TransformCustomizer",
    "TypeCastCustomizer",
    "autosource",
    "register_generator",
    "with_customizer",
    "freeze_param",
]
