"""
Unit tests for ListGenerator.

Tests the decorator pattern implementation where ListGenerator
delegates element generation to appropriate type generators.
"""
import random
from dataclasses import dataclass

import pytest
from typing import List

from autoparameterized.base import TypeGenerator, Customizer
from autoparameterized.generators import ListGenerator
from autoparameterized.decorator import autosource, register_generator, with_customizer


def test_if_sut_generates_int_list_correctly():
    # Arrange
    constraints = {'element_type': int}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    assert isinstance(actual, list)
    assert len(actual) > 0
    for actualElement in actual:
        assert isinstance(actualElement, int)

def test_if_sut_generates_3_elements_by_default():
    # Arrange
    constraints = {'element_type': int}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    assert len(actual) == 3


def test_if_sut_generates_random_elements_correctly():
    # Arrange
    constraints = {'element_type': int}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    distinct_values = set(actual)
    assert len(actual) == len(distinct_values)


def test_if_sut_generates_given_number_of_integers_correctly():
    # Arrange
    num_integers = random.randint(1, 10)
    constraints = {'element_type': int, 'size': num_integers}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    assert len(actual) == num_integers


def test_if_sut_generates_integers_satisfying_given_min_max_constraints():
    # Arrange
    min_value, max_value = 0, 100
    constraints = {
        'element_type': int,
        'element_constraints': {'min_value': min_value, 'max_value': max_value}
    }
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    for actualElement in actual:
        assert min_value <= actualElement <= max_value


def test_if_sut_generates_string_list_correctly():
    # Arrange
    constraints = {'element_type': str}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    assert isinstance(actual, list)
    assert len(actual) == 3
    for actualElement in actual:
        assert isinstance(actualElement, str)


def test_if_sut_generates_strings_of_which_lengths_are_10_by_default():
    # Arrange
    constraints = {'element_type': str}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    for actualElement in actual:
        assert len(actualElement) == 10


def test_if_sut_generates_given_length_of_strings_correctly():
    # Arrange
    length = random.randint(1, 10)
    constraints = {'element_type': str, 'element_constraints': {'length': length}}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    for actualElement in actual:
        assert len(actualElement) == length


def test_if_sut_generates_strings_by_default_if_no_element_type_is_specified():
    # Arrange
    sut = ListGenerator(constraints={})

    # Act
    actual = sut.generate()

    # Assert
    assert isinstance(actual, list)
    assert len(actual) == 3
    for actualElement in actual:
        assert isinstance(actualElement, str)

def test_if_sut_generates_list_of_complex_objects():
    @dataclass
    class ComplexObject:
        foo: List[int]
        bar: str

    # Arrange
    constraints = {'element_type': ComplexObject}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    assert isinstance(actual, list)
    assert len(actual) == 3
    for actualElement in actual:
        assert isinstance(actualElement, ComplexObject)


@autosource
def test_if_sut_generates_int_list_by_decorator_without_constraints_correctly(numbers: List[int]):
    assert isinstance(numbers, list)
    assert len(numbers) == 3
    for actual in numbers:
        assert isinstance(actual, int)


@autosource(numbers__size = 5, numbers__min_value = -10, numbers__max_value = 10)
def test_if_sut_generates_int_list_by_decorator_with_given_constraints_correctly(numbers: List[int]):
    assert isinstance(numbers, list)
    assert len(numbers) == 5
    for actual in numbers:
        assert isinstance(actual, int)
        assert -10 <= actual <= 10

@autosource
def test_if_sut_generates_str_list_by_decorator_without_constraints_correctly(strings: List[str]):
    assert isinstance(strings, list)
    assert len(strings) == 3
    for actual in strings:
        assert isinstance(actual, str)


@autosource(strings__size = 5, strings__length = 15)
def test_if_sut_generates_str_list_by_decorator_with_given_constraints_correctly(strings: List[str]):
    assert isinstance(strings, list)
    assert len(strings) == 5
    for actual in strings:
        assert isinstance(actual, str)
        assert len(actual) == 15

@autosource
def test_if_sut_generates_list_of_lists_correctly(list_of_lists: List[List[int]]):
    assert isinstance(list_of_lists, list)
    assert len(list_of_lists) == 3
    for actual_list in list_of_lists:
        assert isinstance(actual_list, list)

        for actual in actual_list:
            assert isinstance(actual, int)

class PositiveEvenNumberGenerator(TypeGenerator):
    def generate(self) -> int:
        import random
        positive_number = random.randint(0, 1_000_000_000)
        return positive_number - (positive_number % 2)

@autosource
@register_generator(int, PositiveEvenNumberGenerator)
def test_if_sut_generates_list_of_elements_with_given_generator_correctly(numbers: List[int]):
    assert isinstance(numbers, list)
    assert len(numbers) == 3
    for actual in numbers:
        assert isinstance(actual, int)
        assert actual >= 0
        assert (actual % 2) == 0


class DoubleCustomizer(Customizer):
    """Customizer that doubles the input value."""
    def customize(self, value):
        return value * 2


@autosource(numbers__min_value=1, numbers__max_value=10)
@with_customizer('numbers', DoubleCustomizer())
def test_if_sut_generates_list_with_customizer_correctly(numbers: List[int]):
    assert isinstance(numbers, list)
    assert len(numbers) == 3
    for actual in numbers:
        assert isinstance(actual, int)
        # Original range is 1-10, doubled should be 2-20
        assert 2 <= actual <= 20
        assert (actual % 2) == 0  # All doubled values are even
