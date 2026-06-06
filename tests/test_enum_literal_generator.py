"""Tests for EnumGenerator and LiteralGenerator."""

from enum import Enum
from typing import Literal

import pytest

from autoparameterized import (
    EnumGenerator,
    LiteralGenerator,
    autosource,
)
from autoparameterized.resolver import create_resolver


class Status(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"


def test_enum_generator_generates_enum_member():
    generator = EnumGenerator(Status, seed=42)

    value = generator.generate()

    assert isinstance(value, Status)


def test_enum_generator_respects_choices_constraint():
    generator = EnumGenerator(
        Status,
        constraints={'choices': [Status.ACTIVE]},
        seed=42,
    )

    value = generator.generate()

    assert value is Status.ACTIVE


def test_enum_generator_is_reproducible_with_seed():
    first = EnumGenerator(Status, seed=123).generate()
    second = EnumGenerator(Status, seed=123).generate()

    assert first is second


def test_enum_generator_rejects_invalid_enum_type():
    with pytest.raises(ValueError):
        EnumGenerator(str)


def test_resolver_resolves_enum_type():
    generator = create_resolver().resolve(Status)

    assert isinstance(generator, EnumGenerator)

    value = generator.generate()

    assert isinstance(value, Status)


def test_autosource_generates_enum_parameter():
    received_value = None

    @autosource(seed=42)
    def test_func(status: Status):
        nonlocal received_value
        received_value = status

    test_func()

    assert isinstance(received_value, Status)


def test_literal_generator_generates_literal_value():
    generator = LiteralGenerator(choices=("small", "large"), seed=42)

    value = generator.generate()

    assert value in {"small", "large"}


def test_literal_generator_respects_choices_constraint():
    generator = LiteralGenerator(
        choices=("small", "large"),
        constraints={'choices': ("small",)},
        seed=42,
    )

    value = generator.generate()

    assert value == "small"


def test_literal_generator_is_reproducible_with_seed():
    first = LiteralGenerator(choices=(1, 2, 3), seed=123).generate()
    second = LiteralGenerator(choices=(1, 2, 3), seed=123).generate()

    assert first == second


def test_literal_generator_rejects_empty_choices():
    with pytest.raises(ValueError):
        LiteralGenerator().generate()


def test_resolver_resolves_literal_type():
    generator = create_resolver().resolve(Literal["read", "write"], seed=42)

    assert isinstance(generator, LiteralGenerator)

    value = generator.generate()

    assert value in {"read", "write"}


def test_autosource_generates_literal_parameter():
    received_value = None

    @autosource(seed=42)
    def test_func(mode: Literal["read", "write"]):
        nonlocal received_value
        received_value = mode

    test_func()

    assert received_value in {"read", "write"}
