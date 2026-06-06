from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

import pytest

from autoparameterized import (
    autosource,
    BoolGenerator,
    DataclassGenerator,
    DateTimeGenerator,
    DictGenerator,
    FloatGenerator,
)
from autoparameterized.resolver import create_resolver


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


@dataclass
class GeneratedProfile:
    name: str
    age: int


@dataclass
class GeneratedAccount:
    profile: GeneratedProfile
    scores: List[int]
    metadata: Dict[str, int]


def test_dataclass_generator_respects_field_types_and_constraints():
    generator = DataclassGenerator(
        constraints={
            'dataclass_type': GeneratedProfile,
            'field_constraints': {
                'name': {'length': 4},
                'age': {'min_value': 18, 'max_value': 30},
            },
        },
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, GeneratedProfile)
    assert isinstance(value.name, str)
    assert len(value.name) == 4
    assert isinstance(value.age, int)
    assert 18 <= value.age <= 30


def test_dataclass_generator_accepts_flat_field_constraints():
    generator = DataclassGenerator(
        constraints={
            'dataclass_type': GeneratedProfile,
            'name__length': 4,
            'age__min_value': 18,
            'age__max_value': 30,
        },
        seed=42,
    )

    value = generator.generate()

    assert len(value.name) == 4
    assert 18 <= value.age <= 30


def test_dataclass_generator_generates_nested_values():
    generator = DataclassGenerator(
        constraints={
            'dataclass_type': GeneratedAccount,
            'profile__name__length': 5,
            'profile__age__min_value': 20,
            'profile__age__max_value': 40,
            'scores__size': 2,
            'scores__min_value': 10,
            'scores__max_value': 20,
            'metadata__size': 2,
            'metadata__key_length': 3,
            'metadata__value_min_value': 1,
            'metadata__value_max_value': 9,
        },
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, GeneratedAccount)
    assert isinstance(value.profile, GeneratedProfile)
    assert len(value.profile.name) == 5
    assert 20 <= value.profile.age <= 40
    assert len(value.scores) == 2
    assert all(10 <= score <= 20 for score in value.scores)
    assert len(value.metadata) == 2
    assert all(len(key) == 3 for key in value.metadata)
    assert all(1 <= item <= 9 for item in value.metadata.values())


def test_dataclass_generator_is_reproducible_with_seed():
    constraints = {'dataclass_type': GeneratedProfile}

    first = DataclassGenerator(constraints=constraints, seed=123).generate()
    second = DataclassGenerator(constraints=constraints, seed=123).generate()

    assert first == second


def test_dataclass_generator_rejects_missing_dataclass_type():
    with pytest.raises(ValueError):
        DataclassGenerator().generate()


def test_resolver_resolves_dataclass_type():
    resolver = create_resolver()

    generator = resolver.resolve(GeneratedProfile)

    assert isinstance(generator, DataclassGenerator)


def test_autosource_generates_dataclass_values():
    received_value = None

    @autosource(seed=42, value__name__length=4, value__age__min_value=18)
    def test_func(value: GeneratedProfile):
        nonlocal received_value
        received_value = value

    test_func()

    assert isinstance(received_value, GeneratedProfile)
    assert len(received_value.name) == 4
    assert received_value.age >= 18


def test_autosource_generates_list_of_dataclass_values():
    received_value = None

    @autosource(seed=42, values__size=2, values__name__length=4)
    def test_func(values: List[GeneratedProfile]):
        nonlocal received_value
        received_value = values

    test_func()

    assert isinstance(received_value, list)
    assert len(received_value) == 2
    assert all(isinstance(value, GeneratedProfile) for value in received_value)
    assert all(len(value.name) == 4 for value in received_value)
