"""
Unit tests for ListGenerator.

Tests the decorator pattern implementation where ListGenerator
delegates element generation to appropriate type generators.
"""
import random

import pytest
from typing import List

from autoparameterized.generators import ListGenerator


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
        assert actualElement > min_value
        assert actualElement < max_value


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
    constraints = {'element_type': str}
    sut = ListGenerator(constraints = constraints)

    # Act
    actual = sut.generate()

    # Assert
    for actualElement in actual:
        assert len(actualElement) == 10


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

# TODO - DataclassGenerator 가 구현된 이후부터 실행.
def __todo_test_if_sut_generates_list_of_complex_objects():
    class ComplexObject:
        def __init__(self, foo: List[int], bar: str):
            self.foo: List[int] = foo
            self.bar: str = bar

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
