"""Test actual value generation - verify that values are actually generated."""

import pytest
from autoparameterized import autosource


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


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
