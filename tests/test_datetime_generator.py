"""Tests for DateTimeGenerator."""

from datetime import datetime

import pytest

from autoparameterized import DateTimeGenerator


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
