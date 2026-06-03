from datetime import datetime

import pytest

from autoparameterized.base import TypeGenerator
from autoparameterized.decorator import get_generator_for_type, register_generator
from autoparameterized.generators import (
    BoolGenerator,
    DateTimeGenerator,
    FloatGenerator,
    IntGenerator,
    StringGenerator,
)


@pytest.mark.parametrize(
    "param_type, expected_generator",
    [
        (int, IntGenerator),
        (str, StringGenerator),
        (float, FloatGenerator),
        (bool, BoolGenerator),
        (datetime, DateTimeGenerator),
    ],
)
def test_get_generator_for_type_returns_builtin_generator(param_type, expected_generator):
    generator = get_generator_for_type(
        param_type,
        constraints={'example': 'constraint'},
        seed=42,
    )

    assert isinstance(generator, expected_generator)
    assert generator.constraints == {'example': 'constraint'}
    assert generator.seed == 42


def test_get_generator_for_type_rejects_unsupported_type():
    class UnsupportedType:
        pass

    with pytest.raises(TypeError, match="No generator registered"):
        get_generator_for_type(UnsupportedType, constraints={}, seed=None)


def test_register_generator_adds_custom_type_mapping():
    class CustomType:
        pass

    @register_generator(CustomType)
    class CustomTypeGenerator(TypeGenerator):
        def generate(self):
            return CustomType()

    generator = get_generator_for_type(
        CustomType,
        constraints={'key': 'value'},
        seed=123,
    )

    assert isinstance(generator, CustomTypeGenerator)
    assert generator.constraints == {'key': 'value'}
    assert generator.seed == 123
    assert isinstance(generator.generate(), CustomType)


def test_register_generator_returns_original_class():
    class AnotherCustomType:
        pass

    class AnotherCustomTypeGenerator(TypeGenerator):
        def generate(self):
            return AnotherCustomType()

    decorated_class = register_generator(AnotherCustomType)(AnotherCustomTypeGenerator)

    assert decorated_class is AnotherCustomTypeGenerator


def test_register_generator_rejects_non_type_generator_class():
    class InvalidGenerator:
        pass

    with pytest.raises(TypeError, match="TypeGenerator subclass"):
        register_generator(object)(InvalidGenerator)
