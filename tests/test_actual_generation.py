"""Test actual value generation - verify that values are actually generated."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Set, TypedDict

import pytest
from autoparameterized import (
    autosource,
    RangeCustomizer,
    with_customizer,
)


class TestActualIntegerGeneration:
    """Test that integers are actually generated and injected."""

    def test_single_int_parameter(self):
        """Test single integer parameter is generated."""
        received_value = None

        @autosource(seed=42)
        def test_func(value: int):
            nonlocal received_value
            received_value = value

        # Call the decorated function
        test_func()

        # Verify integer was generated and injected
        assert received_value is not None, "No value was generated"
        assert isinstance(received_value, int), f"Expected int, got {type(received_value)}"
        print(f"✓ Generated integer: {received_value}")

    def test_multiple_int_parameters(self):
        """Test multiple integer parameters are generated."""
        received_values = {}

        @autosource(seed=42)
        def test_func(a: int, b: int, c: int):
            nonlocal received_values
            received_values = {'a': a, 'b': b, 'c': c}

        test_func()

        assert len(received_values) == 3, "Not all parameters were generated"
        assert all(isinstance(v, int) for v in received_values.values()), "Not all values are integers"
        print(f"✓ Generated integers: {received_values}")

    def test_int_with_constraints(self):
        """Test integer generation respects constraints."""
        received_value = None

        @autosource(seed=42, value__min_value=10, value__max_value=20)
        def test_func(value: int):
            nonlocal received_value
            received_value = value

        test_func()

        assert received_value is not None
        assert isinstance(received_value, int)
        assert 10 <= received_value <= 20, f"Value {received_value} not in range [10, 20]"
        print(f"✓ Generated integer with constraints: {received_value}")

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same value."""
        value1 = None
        value2 = None

        @autosource(seed=42)
        def test_func1(value: int):
            nonlocal value1
            value1 = value

        @autosource(seed=42)
        def test_func2(value: int):
            nonlocal value2
            value2 = value

        test_func1()
        test_func2()

        assert value1 is not None
        assert value2 is not None
        assert value1 == value2, f"Same seed should produce same value: {value1} != {value2}"
        print(f"✓ Reproducible with seed: {value1} == {value2}")


class TestActualStringGeneration:
    """Test that strings are actually generated and injected."""

    def test_single_string_parameter(self):
        """Test single string parameter is generated."""
        received_value = None

        @autosource(seed=42)
        def test_func(text: str):
            nonlocal received_value
            received_value = text

        test_func()

        assert received_value is not None
        assert isinstance(received_value, str)
        print(f"✓ Generated string: {received_value}")

    def test_string_with_length_constraint(self):
        """Test string generation with length constraint."""
        received_value = None

        @autosource(seed=42, text__length=5)
        def test_func(text: str):
            nonlocal received_value
            received_value = text

        test_func()

        assert received_value is not None
        assert isinstance(received_value, str)
        assert len(received_value) == 5, f"Expected length 5, got {len(received_value)}"
        print(f"✓ Generated string with length constraint: {received_value}")


class TestMixedTypeGeneration:
    """Test generation of mixed types."""

    def test_int_and_string_together(self):
        """Test both int and string parameters together."""
        received_values = {}

        @autosource(seed=42)
        def test_func(age: int, name: str):
            nonlocal received_values
            received_values = {'age': age, 'name': name}

        test_func()

        assert 'age' in received_values
        assert 'name' in received_values
        assert isinstance(received_values['age'], int)
        assert isinstance(received_values['name'], str)
        print(f"✓ Generated mixed types: {received_values}")

    def test_multiple_types_with_constraints(self):
        """Test multiple types with different constraints."""
        received_values = {}

        @autosource(
            seed=42,
            age__min_value=18,
            age__max_value=100,
            name__length=8
        )
        def test_func(age: int, name: str):
            nonlocal received_values
            received_values = {'age': age, 'name': name}

        test_func()

        assert isinstance(received_values['age'], int)
        assert 18 <= received_values['age'] <= 100
        assert isinstance(received_values['name'], str)
        assert len(received_values['name']) == 8
        print(f"✓ Generated with constraints: age={received_values['age']}, name={received_values['name']}")


class TestActualFloatGeneration:
    """Test that floats are actually generated and injected."""

    def test_single_float_parameter(self):
        """Test single float parameter is generated."""
        received_value = None

        @autosource(seed=42)
        def test_func(value: float):
            nonlocal received_value
            received_value = value

        test_func()

        assert received_value is not None
        assert isinstance(received_value, float)
        print(f"✓ Generated float: {received_value}")

    def test_float_with_range_constraint(self):
        """Test float generation with min/max constraints."""
        received_value = None

        @autosource(seed=42, price__min_value=10.0, price__max_value=100.0)
        def test_func(price: float):
            nonlocal received_value
            received_value = price

        test_func()

        assert isinstance(received_value, float)
        assert 10.0 <= received_value <= 100.0
        print(f"✓ Generated float with range: {received_value}")


class TestActualBoolGeneration:
    """Test that booleans are actually generated and injected."""

    def test_single_bool_parameter(self):
        """Test single bool parameter is generated."""
        received_value = None

        @autosource(seed=42)
        def test_func(active: bool):
            nonlocal received_value
            received_value = active

        test_func()

        assert received_value is not None
        assert isinstance(received_value, bool)
        print(f"✓ Generated bool: {received_value}")

    def test_bool_with_probability(self):
        """Test bool with probability constraint."""
        received_value = None

        @autosource(seed=42, flag__probability=1.0)
        def test_func(flag: bool):
            nonlocal received_value
            received_value = flag

        test_func()

        assert received_value is True
        print(f"✓ Generated bool with probability: {received_value}")


class TestActualListGeneration:
    """Test that lists are actually generated and injected."""

    def test_list_of_integers(self):
        """Test list of integers is generated."""
        received_value = None

        @autosource(seed=42, numbers__size=5)
        def test_func(numbers: List[int]):
            nonlocal received_value
            received_value = numbers

        test_func()

        assert received_value is not None
        assert isinstance(received_value, list)
        assert len(received_value) == 5
        assert all(isinstance(x, int) for x in received_value)
        print(f"✓ Generated list: {received_value}")

    def test_list_with_element_constraints(self):
        """Test list with element constraints."""
        received_value = None

        @autosource(seed=42, scores__size=3, scores__min_value=0, scores__max_value=100)
        def test_func(scores: List[int]):
            nonlocal received_value
            received_value = scores

        test_func()

        assert len(received_value) == 3
        assert all(0 <= x <= 100 for x in received_value)
        print(f"✓ Generated list with constraints: {received_value}")


class TestActualSetGeneration:
    """Test that sets are actually generated and injected."""

    def test_set_of_strings(self):
        """Test set of strings is generated."""
        received_value = None

        @autosource(seed=42, tags__size=3)
        def test_func(tags: Set[str]):
            nonlocal received_value
            received_value = tags

        test_func()

        assert received_value is not None
        assert isinstance(received_value, set)
        assert len(received_value) == 3
        assert all(isinstance(x, str) for x in received_value)
        print(f"✓ Generated set: {received_value}")


class TestActualDictGeneration:
    """Test that dicts are actually generated and injected."""

    def test_dict_dynamic_mode(self):
        """Test dynamic dict generation (all keys/values same type)."""
        received_value = None

        @autosource(seed=42, config__size=3)
        def test_func(config: Dict[str, int]):
            nonlocal received_value
            received_value = config

        test_func()

        assert received_value is not None
        assert isinstance(received_value, dict)
        assert len(received_value) == 3
        assert all(isinstance(k, str) for k in received_value.keys())
        assert all(isinstance(v, int) for v in received_value.values())
        print(f"✓ Generated dict (dynamic): {received_value}")

    def test_dict_with_typeddict(self):
        """Test dict generation with TypedDict."""

        class UserInfo(TypedDict):
            name: str
            age: int
            active: bool

        received_value = None

        @autosource(seed=42, user__name__length=6, user__age__min_value=18)
        def test_func(user: UserInfo):
            nonlocal received_value
            received_value = user

        test_func()

        assert received_value is not None
        assert set(received_value.keys()) == {'name', 'age', 'active'}
        assert isinstance(received_value['name'], str)
        assert len(received_value['name']) == 6
        assert isinstance(received_value['age'], int)
        assert received_value['age'] >= 18
        assert isinstance(received_value['active'], bool)
        print(f"✓ Generated dict (TypedDict): {received_value}")


class TestActualDateTimeGeneration:
    """Test that datetimes are actually generated and injected."""

    def test_datetime_parameter(self):
        """Test datetime parameter is generated."""
        received_value = None

        @autosource(seed=42)
        def test_func(timestamp: datetime):
            nonlocal received_value
            received_value = timestamp

        test_func()

        assert received_value is not None
        assert isinstance(received_value, datetime)
        print(f"✓ Generated datetime: {received_value}")

    def test_datetime_with_range(self):
        """Test datetime with min/max constraints."""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        received_value = None

        @autosource(seed=42, created__min_value=start, created__max_value=end)
        def test_func(created: datetime):
            nonlocal received_value
            received_value = created

        test_func()

        assert isinstance(received_value, datetime)
        assert start <= received_value <= end
        print(f"✓ Generated datetime with range: {received_value}")


class TestActualDataclassGeneration:
    """Test that dataclasses are actually generated and injected."""

    def test_simple_dataclass(self):
        """Test simple dataclass generation."""

        @dataclass
        class Person:
            name: str
            age: int

        received_value = None

        @autosource(seed=42, person__name__length=5, person__age__min_value=18)
        def test_func(person: Person):
            nonlocal received_value
            received_value = person

        test_func()

        assert received_value is not None
        assert isinstance(received_value, Person)
        assert isinstance(received_value.name, str)
        assert len(received_value.name) == 5
        assert isinstance(received_value.age, int)
        assert received_value.age >= 18
        print(f"✓ Generated dataclass: {received_value}")

    def test_nested_dataclass(self):
        """Test nested dataclass generation."""

        @dataclass
        class Address:
            city: str
            zipcode: int

        @dataclass
        class Employee:
            name: str
            address: Address

        received_value = None

        @autosource(
            seed=42,
            emp__name__length=8,
            emp__address__city__length=6,
            emp__address__zipcode__min_value=10000,
            emp__address__zipcode__max_value=99999,
        )
        def test_func(emp: Employee):
            nonlocal received_value
            received_value = emp

        test_func()

        assert received_value is not None
        assert isinstance(received_value, Employee)
        assert isinstance(received_value.address, Address)
        assert len(received_value.name) == 8
        assert len(received_value.address.city) == 6
        assert 10000 <= received_value.address.zipcode <= 99999
        print(f"✓ Generated nested dataclass: {received_value}")


class TestDefaultGeneration:
    """Test that generators work without any constraints (using defaults)."""

    def test_int_default_generation(self):
        """Test int generation without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(value: int):
            nonlocal received_value
            received_value = value

        test_func()

        assert received_value is not None
        assert isinstance(received_value, int)
        assert 0 <= received_value <= 100  # default range
        print(f"✓ Default int (0-100): {received_value}")

    def test_string_default_generation(self):
        """Test string generation without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(text: str):
            nonlocal received_value
            received_value = text

        test_func()

        assert received_value is not None
        assert isinstance(received_value, str)
        assert len(received_value) == 10  # default length
        print(f"✓ Default string (length 10): {received_value}")

    def test_float_default_generation(self):
        """Test float generation without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(value: float):
            nonlocal received_value
            received_value = value

        test_func()

        assert received_value is not None
        assert isinstance(received_value, float)
        assert 0.0 <= received_value <= 100.0  # default range
        print(f"✓ Default float (0.0-100.0): {received_value:.2f}")

    def test_bool_default_generation(self):
        """Test bool generation without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(flag: bool):
            nonlocal received_value
            received_value = flag

        test_func()

        assert received_value is not None
        assert isinstance(received_value, bool)
        print(f"✓ Default bool (probability 0.5): {received_value}")

    def test_list_default_generation(self):
        """Test list generation without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(items: List[str]):
            nonlocal received_value
            received_value = items

        test_func()

        assert received_value is not None
        assert isinstance(received_value, list)
        assert len(received_value) == 3  # default size
        assert all(isinstance(x, str) for x in received_value)
        print(f"✓ Default list (size 3): {received_value}")

    def test_set_default_generation(self):
        """Test set generation without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(items: Set[int]):
            nonlocal received_value
            received_value = items

        test_func()

        assert received_value is not None
        assert isinstance(received_value, set)
        assert len(received_value) == 3  # default size
        assert all(isinstance(x, int) for x in received_value)
        print(f"✓ Default set (size 3): {received_value}")

    def test_dict_default_generation(self):
        """Test dict generation without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(mapping: Dict[str, str]):
            nonlocal received_value
            received_value = mapping

        test_func()

        assert received_value is not None
        assert isinstance(received_value, dict)
        assert len(received_value) == 3  # default size
        assert all(isinstance(k, str) for k in received_value.keys())
        assert all(isinstance(v, str) for v in received_value.values())
        print(f"✓ Default dict (size 3): {list(received_value.keys())}")

    def test_datetime_default_generation(self):
        """Test datetime generation without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(timestamp: datetime):
            nonlocal received_value
            received_value = timestamp

        test_func()

        assert received_value is not None
        assert isinstance(received_value, datetime)
        # Default range: 1970-01-01 to 2030-12-31
        assert datetime(1970, 1, 1) <= received_value <= datetime(2030, 12, 31, 23, 59, 59)
        print(f"✓ Default datetime (1970-2030): {received_value}")

    def test_dataclass_default_generation(self):
        """Test dataclass generation without any field constraints."""

        @dataclass
        class SimpleUser:
            username: str
            age: int
            balance: float
            active: bool

        received_value = None

        @autosource(seed=42)
        def test_func(user: SimpleUser):
            nonlocal received_value
            received_value = user

        test_func()

        assert received_value is not None
        assert isinstance(received_value, SimpleUser)
        assert isinstance(received_value.username, str)
        assert len(received_value.username) == 10  # default string length
        assert isinstance(received_value.age, int)
        assert 0 <= received_value.age <= 100  # default int range
        assert isinstance(received_value.balance, float)
        assert 0.0 <= received_value.balance <= 100.0  # default float range
        assert isinstance(received_value.active, bool)
        print(f"✓ Default dataclass: username={received_value.username}, "
              f"age={received_value.age}, balance={received_value.balance:.2f}, "
              f"active={received_value.active}")

    def test_nested_collection_default_generation(self):
        """Test nested collections without constraints."""
        received_value = None

        @autosource(seed=42)
        def test_func(data: List[Dict[str, int]]):
            nonlocal received_value
            received_value = data

        test_func()

        assert received_value is not None
        assert isinstance(received_value, list)
        assert len(received_value) == 3  # default list size
        assert all(isinstance(x, dict) for x in received_value)
        assert all(len(x) == 3 for x in received_value)  # default dict size
        print(f"✓ Default nested List[Dict[str, int]] (size 3x3): "
              f"{[list(d.keys()) for d in received_value]}")

    def test_multiple_types_no_constraints(self):
        """Test multiple different types without any constraints."""
        received_values = {}

        @autosource(seed=42)
        def test_func(
            count: int,
            name: str,
            price: float,
            enabled: bool,
            tags: List[str],
        ):
            nonlocal received_values
            received_values = {
                'count': count,
                'name': name,
                'price': price,
                'enabled': enabled,
                'tags': tags,
            }

        test_func()

        assert isinstance(received_values['count'], int)
        assert 0 <= received_values['count'] <= 100
        assert isinstance(received_values['name'], str)
        assert len(received_values['name']) == 10
        assert isinstance(received_values['price'], float)
        assert 0.0 <= received_values['price'] <= 100.0
        assert isinstance(received_values['enabled'], bool)
        assert isinstance(received_values['tags'], list)
        assert len(received_values['tags']) == 3
        print(f"✓ Multiple types with defaults: count={received_values['count']}, "
              f"name={received_values['name']}, price={received_values['price']:.2f}, "
              f"enabled={received_values['enabled']}, tags={received_values['tags']}")


class TestActualCustomizerUsage:
    """Test that customizers actually work with generation."""

    def test_range_customizer_manual_usage(self):
        """Test RangeCustomizer manual usage (not integrated with @autosource yet)."""
        from autoparameterized import IntGenerator

        # Generate a value that might be out of range
        generator = IntGenerator(constraints={'min_value': -100, 'max_value': 200}, seed=42)
        generated = generator.generate()

        # Apply customizer manually
        customizer = RangeCustomizer(min_value=0, max_value=50)
        clamped = customizer.customize(generated)

        assert 0 <= clamped <= 50
        print(f"✓ RangeCustomizer clamped {generated} to {clamped}")

    def test_multiple_types_real_world_scenario(self):
        """Test a real-world scenario with multiple types."""

        @dataclass
        class Product:
            name: str
            price: float
            tags: List[str]

        received_value = None

        @autosource(
            seed=42,
            product__name__length=10,
            product__price__min_value=1.0,
            product__price__max_value=100.0,
            product__tags__size=3,
            product__tags__length=5,
        )
        def test_func(product: Product):
            nonlocal received_value
            received_value = product

        test_func()

        assert received_value is not None
        assert isinstance(received_value, Product)
        assert len(received_value.name) == 10
        assert 1.0 <= received_value.price <= 100.0
        assert len(received_value.tags) == 3
        assert all(len(tag) == 5 for tag in received_value.tags)
        print(f"✓ Generated complex product: name={received_value.name}, "
              f"price={received_value.price:.2f}, tags={received_value.tags}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
