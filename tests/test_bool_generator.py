"""Tests for BoolGenerator."""

from autoparameterized import BoolGenerator


def test_bool_generator_returns_boolean():
    value = BoolGenerator(seed=42).generate()

    assert isinstance(value, bool)


def test_bool_generator_probability_constraint():
    assert BoolGenerator(constraints={'probability': 1.0}, seed=42).generate() is True
    assert BoolGenerator(constraints={'probability': 0.0}, seed=42).generate() is False


def test_bool_generator_is_reproducible_with_seed():
    first = BoolGenerator(seed=123).generate()
    second = BoolGenerator(seed=123).generate()

    assert first == second
