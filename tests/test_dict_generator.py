"""Tests for DictGenerator."""

from typing import Dict, TypedDict

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


# ============================================================================
# Schema mode tests
# ============================================================================

def test_dict_generator_schema_mode_with_types():
    """Test schema mode with just types."""
    generator = DictGenerator(
        schema={
            'name': str,
            'age': int,
            'active': bool,
        },
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, dict)
    assert set(value.keys()) == {'name', 'age', 'active'}
    assert isinstance(value['name'], str)
    assert isinstance(value['age'], int)
    assert isinstance(value['active'], bool)


def test_dict_generator_schema_mode_with_constraints():
    """Test schema mode with type and constraints."""
    generator = DictGenerator(
        schema={
            'name': {'type': str, 'length': 5},
            'age': {'type': int, 'min_value': 18, 'max_value': 100},
            'score': {'type': float, 'min_value': 0.0, 'max_value': 100.0},
        },
        seed=42,
    )

    value = generator.generate()

    assert len(value['name']) == 5
    assert 18 <= value['age'] <= 100
    assert 0.0 <= value['score'] <= 100.0


def test_dict_generator_schema_mode_with_flat_constraints():
    """Test schema mode with param__constraint style."""
    generator = DictGenerator(
        schema={
            'name': str,
            'age': int,
        },
        constraints={
            'name__length': 8,
            'age__min_value': 25,
            'age__max_value': 50,
        },
        seed=42,
    )

    value = generator.generate()

    assert len(value['name']) == 8
    assert 25 <= value['age'] <= 50


def test_dict_generator_schema_is_reproducible():
    """Test that schema mode is reproducible with same seed."""
    schema = {
        'name': str,
        'age': int,
    }

    first = DictGenerator(schema=schema, seed=123).generate()
    second = DictGenerator(schema=schema, seed=123).generate()

    assert first == second


# ============================================================================
# TypedDict mode tests
# ============================================================================

class UserProfile(TypedDict):
    """Example TypedDict for testing."""
    name: str
    age: int
    active: bool


class ProductInfo(TypedDict):
    """TypedDict with various types."""
    title: str
    price: float
    in_stock: bool
    quantity: int


def test_dict_generator_typeddict_mode_basic():
    """Test TypedDict mode extracts correct schema."""
    generator = DictGenerator(
        typed_dict=UserProfile,
        seed=42,
    )

    value = generator.generate()

    assert isinstance(value, dict)
    assert set(value.keys()) == {'name', 'age', 'active'}
    assert isinstance(value['name'], str)
    assert isinstance(value['age'], int)
    assert isinstance(value['active'], bool)


def test_dict_generator_typeddict_with_target_type_alias():
    """Test TypedDict mode with constraints."""
    generator = DictGenerator(
        typed_dict=UserProfile,
        constraints={'name__length': 6},
        seed=42,
    )

    value = generator.generate()

    assert set(value.keys()) == {'name', 'age', 'active'}
    assert len(value['name']) == 6


def test_dict_generator_typeddict_with_constraints():
    """Test TypedDict mode with field constraints."""
    generator = DictGenerator(
        typed_dict=ProductInfo,
        constraints={
            'title__length': 10,
            'price__min_value': 10.0,
            'price__max_value': 100.0,
            'quantity__min_value': 1,
            'quantity__max_value': 50,
        },
        seed=42,
    )

    value = generator.generate()

    assert len(value['title']) == 10
    assert 10.0 <= value['price'] <= 100.0
    assert 1 <= value['quantity'] <= 50


def test_dict_generator_typeddict_is_reproducible():
    """Test that TypedDict mode is reproducible."""
    first = DictGenerator(typed_dict=UserProfile, seed=123).generate()
    second = DictGenerator(typed_dict=UserProfile, seed=123).generate()

    assert first == second


def test_autosource_with_typeddict():
    """Test @autosource with TypedDict parameter."""
    received_value = None

    @autosource(seed=42, user__name__length=5, user__age__min_value=20)
    def test_func(user: UserProfile):
        nonlocal received_value
        received_value = user

    test_func()

    assert isinstance(received_value, dict)
    assert set(received_value.keys()) == {'name', 'age', 'active'}
    assert len(received_value['name']) == 5
    assert received_value['age'] >= 20
