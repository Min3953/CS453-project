"""Tests for TupleGenerator."""

from typing import Tuple

from autoparameterized import TupleGenerator, autosource, with_customizer
from autoparameterized.base import Customizer
from autoparameterized.resolver import create_resolver


def test_tuple_generator_generates_homogeneous_tuple():
    generator = TupleGenerator(
        constraints={
            'element_type': int,
            'size': 4,
            'element_constraints': {'min_value': 1, 'max_value': 10},
        },
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, tuple)
    assert len(value) == 4
    assert all(isinstance(item, int) for item in value)
    assert all(1 <= item <= 10 for item in value)


def test_tuple_generator_generates_fixed_shape_tuple():
    generator = TupleGenerator(
        constraints={
            'element_types': (int, str, bool),
            '0__min_value': 10,
            '0__max_value': 20,
            '1__length': 5,
            '2__probability': 1.0,
        },
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, tuple)
    assert len(value) == 3
    assert isinstance(value[0], int)
    assert 10 <= value[0] <= 20
    assert isinstance(value[1], str)
    assert len(value[1]) == 5
    assert value[2] is True


def test_tuple_generator_is_reproducible_with_seed():
    constraints = {
        'element_type': int,
        'size': 3,
        'element_constraints': {'min_value': 1, 'max_value': 100},
    }

    first = TupleGenerator(constraints=constraints, seed=123).generate()
    second = TupleGenerator(constraints=constraints, seed=123).generate()

    assert first == second


def test_resolver_resolves_fixed_shape_tuple():
    generator = create_resolver().resolve(Tuple[int, str])

    assert isinstance(generator, TupleGenerator)

    value = generator.generate()

    assert isinstance(value, tuple)
    assert len(value) == 2
    assert isinstance(value[0], int)
    assert isinstance(value[1], str)


def test_resolver_resolves_homogeneous_tuple():
    generator = create_resolver().resolve(
        Tuple[int, ...],
        constraints={'size': 5, 'min_value': 1, 'max_value': 10},
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, tuple)
    assert len(value) == 5
    assert all(isinstance(item, int) for item in value)
    assert all(1 <= item <= 10 for item in value)


def test_autosource_generates_fixed_shape_tuple_with_index_constraints():
    received_value = None

    @autosource(seed=42, pair__0__min_value=10, pair__0__max_value=20, pair__1__length=4)
    def test_func(pair: Tuple[int, str]):
        nonlocal received_value
        received_value = pair

    test_func()

    assert isinstance(received_value, tuple)
    assert len(received_value) == 2
    assert 10 <= received_value[0] <= 20
    assert isinstance(received_value[1], str)
    assert len(received_value[1]) == 4


def test_autosource_generates_homogeneous_tuple_with_size_constraint():
    received_value = None

    @autosource(seed=42, values__size=4, values__min_value=1, values__max_value=10)
    def test_func(values: Tuple[int, ...]):
        nonlocal received_value
        received_value = values

    test_func()

    assert isinstance(received_value, tuple)
    assert len(received_value) == 4
    assert all(1 <= item <= 10 for item in received_value)


class DoubleCustomizer(Customizer):
    def customize(self, value):
        return value * 2


@autosource(values__size=3, values__min_value=1, values__max_value=10)
@with_customizer('values', DoubleCustomizer())
def test_autosource_applies_customizer_to_tuple_elements(values: Tuple[int, ...]):
    assert isinstance(values, tuple)
    assert len(values) == 3
    assert all(2 <= item <= 20 for item in values)
    assert all((item % 2) == 0 for item in values)
