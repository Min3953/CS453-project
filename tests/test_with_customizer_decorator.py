"""
Unit tests for with_customizer decorator.

Tests that customizers work with various parameter types:
- Simple types (int, str, float)
- Collection types (List, Set)
- Multiple parameters
- Multiple executions (count > 1)
"""
from typing import List, Set

from autoparameterized.base import Customizer
from autoparameterized.decorator import autosource, with_customizer


class DoubleCustomizer(Customizer):
    """Customizer that doubles the input value."""
    def customize(self, value):
        return value * 2


class UpperCaseCustomizer(Customizer):
    """Customizer that converts string to uppercase."""
    def customize(self, value):
        return value.upper()


class RoundCustomizer(Customizer):
    """Customizer that rounds float to nearest integer."""
    def customize(self, value):
        return round(value)


class AddPrefixCustomizer(Customizer):
    """Customizer that adds a prefix to a string."""
    def __init__(self, prefix: str):
        self.prefix = prefix

    def customize(self, value):
        return f"{self.prefix}{value}"


# ============================================================================
# Simple type tests
# ============================================================================

@autosource(value__min_value=1, value__max_value=10)
@with_customizer('value', DoubleCustomizer())
def test_if_sut_applies_customizer_to_int_parameter_correctly(value: int):
    assert isinstance(value, int)
    # Original range is 1-10, doubled should be 2-20
    assert 2 <= value <= 20
    assert (value % 2) == 0  # All doubled values are even


@autosource(text__length=5)
@with_customizer('text', UpperCaseCustomizer())
def test_if_sut_applies_customizer_to_str_parameter_correctly(text: str):
    assert isinstance(text, str)
    assert len(text) == 5
    assert text.isupper()  # Should be all uppercase


@autosource(value__min_value=1.0, value__max_value=10.0)
@with_customizer('value', RoundCustomizer())
def test_if_sut_applies_customizer_to_float_parameter_correctly(value: float):
    # After rounding, should be an integer value
    assert isinstance(value, (int, float))
    assert value == int(value)  # Should be a whole number
    assert 1 <= value <= 10


# ============================================================================
# Multiple parameters tests
# ============================================================================

@autosource(age__min_value=10, age__max_value=20, name__length=5)
@with_customizer('age', DoubleCustomizer())
@with_customizer('name', UpperCaseCustomizer())
def test_if_sut_applies_different_customizers_to_multiple_parameters_correctly(age: int, name: str):
    assert isinstance(age, int)
    assert isinstance(name, str)
    # Age: original 10-20, doubled should be 20-40
    assert 20 <= age <= 40
    assert (age % 2) == 0
    # Name: should be uppercase
    assert len(name) == 5
    assert name.isupper()


# ============================================================================
# Count parameter tests
# ============================================================================

@autosource(count=3, value__min_value=5, value__max_value=15)
@with_customizer('value', DoubleCustomizer())
def test_if_sut_applies_customizer_with_count_parameter_correctly(value: int):
    assert isinstance(value, int)
    # Original range is 5-15, doubled should be 10-30
    assert 10 <= value <= 30
    assert (value % 2) == 0


# ============================================================================
# Collection type tests
# ============================================================================

@autosource(numbers__size=4, numbers__min_value=1, numbers__max_value=10)
@with_customizer('numbers', DoubleCustomizer())
def test_if_sut_applies_customizer_to_list_elements_correctly(numbers: List[int]):
    assert isinstance(numbers, list)
    assert len(numbers) == 4
    for actual in numbers:
        assert isinstance(actual, int)
        # Original range is 1-10, doubled should be 2-20
        assert 2 <= actual <= 20
        assert (actual % 2) == 0


@autosource(numbers__size=3, numbers__min_value=1, numbers__max_value=10)
@with_customizer('numbers', DoubleCustomizer())
def test_if_sut_applies_customizer_to_set_elements_correctly(numbers: Set[int]):
    assert isinstance(numbers, set)
    assert len(numbers) == 3
    for actual in numbers:
        assert isinstance(actual, int)
        # Original range is 1-10, doubled should be 2-20
        assert 2 <= actual <= 20
        assert (actual % 2) == 0


# ============================================================================
# Customizer with parameters test
# ============================================================================

@autosource(name__length=5)
@with_customizer('name', AddPrefixCustomizer(prefix="TEST_"))
def test_if_sut_applies_customizer_with_constructor_parameters_correctly(name: str):
    assert isinstance(name, str)
    assert name.startswith("TEST_")
    # Original length 5 + prefix "TEST_" (5 chars) = 10 total
    assert len(name) == 10
