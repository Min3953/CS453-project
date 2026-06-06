"""Tests for DateGenerator."""

from datetime import date

import pytest

from autoparameterized import DateGenerator, autosource
from autoparameterized.resolver import create_resolver


def test_date_generator_respects_range():
    start = date(2024, 1, 1)
    end = date(2024, 1, 31)
    generator = DateGenerator(
        constraints={'min_value': start, 'max_value': end},
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, date)
    assert start <= value <= end


def test_date_generator_accepts_start_end_aliases():
    start = date(2024, 1, 1)
    end = date(2024, 1, 31)
    generator = DateGenerator(
        constraints={'start': start, 'end': end},
        seed=42,
    )

    value = generator.generate()

    assert start <= value <= end


def test_date_generator_is_reproducible_with_seed():
    constraints = {
        'min_value': date(2024, 1, 1),
        'max_value': date(2024, 1, 31),
    }

    first = DateGenerator(constraints=constraints, seed=123).generate()
    second = DateGenerator(constraints=constraints, seed=123).generate()

    assert first == second


def test_date_generator_rejects_invalid_range():
    with pytest.raises(ValueError):
        DateGenerator(
            constraints={
                'min_value': date(2024, 1, 31),
                'max_value': date(2024, 1, 1),
            }
        ).generate()


def test_resolver_resolves_date_type():
    generator = create_resolver().resolve(date)

    assert isinstance(generator, DateGenerator)


def test_autosource_generates_date_parameter():
    received_value = None

    @autosource(seed=42)
    def test_func(value: date):
        nonlocal received_value
        received_value = value

    test_func()

    assert isinstance(received_value, date)
