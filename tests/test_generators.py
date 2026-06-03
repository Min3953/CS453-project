from datetime import datetime

import pytest

from autoparameterized import BoolGenerator, DateTimeGenerator, FloatGenerator


def test_float_generator_respects_range():
    generator = FloatGenerator(
        constraints={'min_value': 1.5, 'max_value': 2.5},
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, float)
    assert 1.5 <= value <= 2.5


def test_float_generator_is_reproducible_with_seed():
    first = FloatGenerator(seed=123).generate()
    second = FloatGenerator(seed=123).generate()

    assert first == second


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


def test_datetime_generator_respects_range():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 31)
    generator = DateTimeGenerator(
        constraints={'min_value': start, 'max_value': end},
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, datetime)
    assert start <= value <= end


def test_datetime_generator_accepts_start_end_aliases():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 31)
    generator = DateTimeGenerator(
        constraints={'start': start, 'end': end},
        seed=42,
    )

    value = generator.generate()

    assert start <= value <= end


def test_datetime_generator_is_reproducible_with_seed():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 31)
    constraints = {'min_value': start, 'max_value': end}

    first = DateTimeGenerator(constraints=constraints, seed=123).generate()
    second = DateTimeGenerator(constraints=constraints, seed=123).generate()

    assert first == second


def test_datetime_generator_rejects_invalid_range():
    with pytest.raises(ValueError):
        DateTimeGenerator(
            constraints={
                'min_value': datetime(2024, 1, 31),
                'max_value': datetime(2024, 1, 1),
            },
        ).generate()
