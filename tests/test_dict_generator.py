"""Tests for DictGenerator."""

from typing import Dict

from autoparameterized import autosource, DictGenerator
from autoparameterized.resolver import create_resolver


def test_dict_generator_respects_key_and_value_types():
    generator = DictGenerator(
        constraints={'key_type': str, 'value_type': int},
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, dict)
    assert len(value) == 3
    assert all(isinstance(key, str) for key in value)
    assert all(isinstance(item, int) for item in value.values())


def test_dict_generator_respects_nested_constraints():
    generator = DictGenerator(
        constraints={
            'key_type': str,
            'value_type': int,
            'size': 5,
            'key_constraints': {'length': 4},
            'value_constraints': {'min_value': 10, 'max_value': 20},
        },
        seed=42,
    )

    value = generator.generate()

    assert len(value) == 5
    assert all(len(key) == 4 for key in value)
    assert all(10 <= item <= 20 for item in value.values())


def test_dict_generator_is_reproducible_with_seed():
    constraints = {'key_type': str, 'value_type': int}

    first = DictGenerator(constraints=constraints, seed=123).generate()
    second = DictGenerator(constraints=constraints, seed=123).generate()

    assert first == second


def test_resolver_resolves_dict_type():
    resolver = create_resolver()

    generator = resolver.resolve(Dict[str, int])

    assert isinstance(generator, DictGenerator)


def test_resolver_resolves_bare_dict_type():
    resolver = create_resolver()

    generator = resolver.resolve(dict)
    value = generator.generate()

    assert isinstance(generator, DictGenerator)
    assert isinstance(value, dict)
    assert all(isinstance(key, str) for key in value)
    assert all(isinstance(item, str) for item in value.values())


def test_resolver_relays_dict_constraints():
    resolver = create_resolver()

    generator = resolver.resolve(
        Dict[str, int],
        constraints={
            'size': 2,
            'key_length': 3,
            'value_min_value': 10,
            'value_max_value': 20,
        },
        seed=42,
    )
    value = generator.generate()

    assert len(value) == 2
    assert all(len(key) == 3 for key in value)
    assert all(10 <= item <= 20 for item in value.values())


def test_resolver_accepts_dict_constraint_maps():
    resolver = create_resolver()

    generator = resolver.resolve(
        Dict[str, int],
        constraints={
            'key_constraints': {'length': 3},
            'value_constraints': {'min_value': 10, 'max_value': 20},
        },
        seed=42,
    )
    value = generator.generate()

    assert generator.constraints['key_constraints'] == {'length': 3}
    assert generator.constraints['value_constraints'] == {
        'min_value': 10,
        'max_value': 20,
    }
    assert all(len(key) == 3 for key in value)
    assert all(10 <= item <= 20 for item in value.values())


def test_autosource_generates_dict_values():
    received_value = None

    @autosource(seed=42, value__size=2, value__key_length=3)
    def test_func(value: Dict[str, int]):
        nonlocal received_value
        received_value = value

    test_func()

    assert isinstance(received_value, dict)
    assert len(received_value) == 2
    assert all(isinstance(key, str) for key in received_value)
    assert all(len(key) == 3 for key in received_value)
    assert all(isinstance(item, int) for item in received_value.values())
