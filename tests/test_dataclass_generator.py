"""Tests for DataclassGenerator."""

from dataclasses import dataclass
from typing import Dict, List

import pytest

from autoparameterized import autosource, DataclassGenerator
from autoparameterized.resolver import create_resolver


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
        dataclass_type=GeneratedProfile,
        constraints={
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
        dataclass_type=GeneratedProfile,
        constraints={
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
        dataclass_type=GeneratedAccount,
        constraints={
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
    first = DataclassGenerator(dataclass_type=GeneratedProfile, seed=123).generate()
    second = DataclassGenerator(dataclass_type=GeneratedProfile, seed=123).generate()

    assert first == second


def test_dataclass_generator_rejects_invalid_dataclass_type():
    with pytest.raises(ValueError):
        DataclassGenerator(dataclass_type=str)  # str is not a dataclass


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
