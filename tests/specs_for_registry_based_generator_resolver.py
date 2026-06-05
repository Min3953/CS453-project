"""
Unit tests for RegistryBasedGeneratorResolver.

Tests the type resolution system that maps types to their generators.
"""

import pytest
from typing import List

from autoparameterized.resolver import create_resolver, RegistryBasedGeneratorResolver
from autoparameterized.generators import IntGenerator, StringGenerator, ListGenerator
from autoparameterized.base import TypeGenerator


def test_if_sut_resolves_int_type_correctly():
    # Arrange
    sut = create_resolver()

    # Act
    actual = sut.resolve(int)

    # Assert
    assert isinstance(actual, IntGenerator)


def test_if_sut_resolves_str_type_correctly():
    # Arrange
    sut = create_resolver()

    # Act
    actual = sut.resolve(str)

    # Assert
    assert isinstance(actual, StringGenerator)


def test_if_sut_resolves_list_of_int_correctly():
    # Arrange
    sut = create_resolver()

    # Act
    actual = sut.resolve(List[int])

    # Assert
    assert isinstance(actual, ListGenerator)


def test_if_sut_resolves_list_of_str_correctly():
    # Arrange
    sut = create_resolver()

    # Act
    actual = sut.resolve(List[str])

    # Assert
    assert isinstance(actual, ListGenerator)


def test_if_sut_relays_constraints_to_resolved_generator():
    # Arrange
    sut = create_resolver()
    constraints = {'min_value': 10, 'max_value': 20}

    # Act
    actual = sut.resolve(int, constraints=constraints)

    # Assert
    assert actual.constraints == constraints


def test_if_sut_raises_error_for_unregistered_type():
    # Arrange
    sut = create_resolver()

    class UnregisteredType:
        pass

    # Act & Assert
    with pytest.raises(ValueError):
        sut.resolve(UnregisteredType)
