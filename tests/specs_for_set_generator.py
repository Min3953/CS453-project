"""
Unit tests for SetGenerator.

Tests the decorator pattern implementation where SetGenerator
delegates element generation to appropriate type generators.
"""
import random

import pytest
from typing import Set

from autoparameterized.base import TypeGenerator
from autoparameterized.generators import SetGenerator
from autoparameterized.decorator import autosource, register_generator


def test_if_sut_generates_int_set_correctly():
    # Arrange
    constraints = {'element_type': int}
    sut = SetGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    assert isinstance(actual, set)
    assert len(actual) > 0
    for actualElement in actual:
        assert isinstance(actualElement, int)

def test_if_sut_generates_3_elements_by_default():
    # Arrange
    constraints = {'element_type': int}
    sut = SetGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    assert len(actual) == 3


def test_if_sut_generates_distinct_elements():
    # Arrange
    constraints = {'element_type': int, 'size': 10}
    sut = SetGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    # Sets automatically have distinct elements
    assert len(actual) == 10


def test_if_sut_generates_given_number_of_integers_correctly():
    # Arrange
    num_integers = random.randint(1, 10)
    constraints = {'element_type': int, 'size': num_integers}
    sut = SetGenerator(constraints = constraints)

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
    sut = SetGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    for actualElement in actual:
        assert min_value <= actualElement <= max_value


def test_if_sut_generates_string_set_correctly():
    # Arrange
    constraints = {'element_type': str}
    sut = SetGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    assert isinstance(actual, set)
    assert len(actual) == 3
    for actualElement in actual:
        assert isinstance(actualElement, str)


def test_if_sut_generates_strings_of_which_lengths_are_10_by_default():
    # Arrange
    constraints = {'element_type': str}
    sut = SetGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    for actualElement in actual:
        assert len(actualElement) == 10


def test_if_sut_generates_given_length_of_strings_correctly():
    # Arrange
    length = random.randint(1, 10)
    constraints = {'element_type': str, 'element_constraints': {'length': length}}
    sut = SetGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    for actualElement in actual:
        assert len(actualElement) == length


def test_if_sut_generates_strings_by_default_if_no_element_type_is_specified():
    # Arrange
    sut = SetGenerator(constraints={})

    # Act
    actual = sut.generate()

    # Assert
    assert isinstance(actual, set)
    assert len(actual) == 3
    for actualElement in actual:
        assert isinstance(actualElement, str)


@autosource
def test_if_sut_generates_int_set_by_decorator_without_constraints_correctly(numbers: Set[int]):
    assert isinstance(numbers, set)
    assert len(numbers) == 3
    for actual in numbers:
        assert isinstance(actual, int)


@autosource(numbers__size = 5, numbers__min_value = -10, numbers__max_value = 10)
def test_if_sut_generates_int_set_by_decorator_with_given_constraints_correctly(numbers: Set[int]):
    assert isinstance(numbers, set)
    assert len(numbers) == 5
    for actual in numbers:
        assert isinstance(actual, int)
        assert -10 <= actual <= 10

@autosource
def test_if_sut_generates_str_set_by_decorator_without_constraints_correctly(strings: Set[str]):
    assert isinstance(strings, set)
    assert len(strings) == 3
    for actual in strings:
        assert isinstance(actual, str)


@autosource(strings__size = 5, strings__length = 15)
def test_if_sut_generates_str_set_by_decorator_with_given_constraints_correctly(strings: Set[str]):
    assert isinstance(strings, set)
    assert len(strings) == 5
    for actual in strings:
        assert isinstance(actual, str)
        assert len(actual) == 15


@autosource
def test_if_sut_generates_str_set_by_default_if_element_type_is_not_specified(strings: Set):
    assert isinstance(strings, set)
    assert len(strings) == 3
    for actual in strings:
        assert isinstance(actual, str)


class PositiveOddNumberGenerator(TypeGenerator):
    def generate(self) -> int:
        import random
        positive_number = random.randint(0, 1_000_000_000)
        return positive_number if (positive_number % 2) == 1 else positive_number + 1

@autosource
@register_generator(int, PositiveOddNumberGenerator)
def test_if_sut_generates_set_of_elements_with_given_generator_correctly(numbers: Set[int]):
    assert isinstance(numbers, set)
    assert len(numbers) == 3
    for actual in numbers:
        assert isinstance(actual, int)
        assert actual > 0
        assert (actual % 2) == 1
