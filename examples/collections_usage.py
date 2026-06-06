"""Collection types usage examples for autoparameterized."""

from typing import Dict, List, Set

from autoparameterized import autosource


def test_list_of_integers():
    """Generate a list of integers."""
    received_value = None

    @autosource(seed=42, numbers__size=5)
    def test_func(numbers: List[int]):
        nonlocal received_value
        received_value = numbers

    test_func()

    print(f"Generated list: {received_value}")
    assert len(received_value) == 5
    assert all(isinstance(n, int) for n in received_value)


def test_list_with_element_constraints():
    """Generate a list with constraints on elements."""
    received_value = None

    @autosource(
        seed=42,
        scores__size=3,
        scores__min_value=0,
        scores__max_value=100
    )
    def test_func(scores: List[int]):
        nonlocal received_value
        received_value = scores

    test_func()

    print(f"Generated scores: {received_value}")
    assert len(received_value) == 3
    assert all(0 <= score <= 100 for score in received_value)


def test_list_of_strings():
    """Generate a list of strings with specific length."""
    received_value = None

    @autosource(seed=42, tags__size=4, tags__length=6)
    def test_func(tags: List[str]):
        nonlocal received_value
        received_value = tags

    test_func()

    print(f"Generated tags: {received_value}")
    assert len(received_value) == 4
    assert all(len(tag) == 6 for tag in received_value)


def test_set_of_strings():
    """Generate a set of unique strings."""
    received_value = None

    @autosource(seed=42, categories__size=3, categories__length=5)
    def test_func(categories: Set[str]):
        nonlocal received_value
        received_value = categories

    test_func()

    print(f"Generated set: {received_value}")
    assert len(received_value) == 3
    assert all(len(cat) == 5 for cat in received_value)


def test_dict_basic():
    """Generate a dictionary with specific types."""
    received_value = None

    @autosource(seed=42, metadata__size=3, metadata__key_length=4)
    def test_func(metadata: Dict[str, int]):
        nonlocal received_value
        received_value = metadata

    test_func()

    print(f"Generated dict: {received_value}")
    assert len(received_value) == 3
    assert all(len(key) == 4 for key in received_value.keys())
    assert all(isinstance(val, int) for val in received_value.values())


def test_dict_with_value_constraints():
    """Generate a dictionary with constraints on both keys and values."""
    received_value = None

    @autosource(
        seed=42,
        scores__size=4,
        scores__key_length=3,
        scores__value_min_value=50,
        scores__value_max_value=100
    )
    def test_func(scores: Dict[str, int]):
        nonlocal received_value
        received_value = scores

    test_func()

    print(f"Generated scores dict: {received_value}")
    assert len(received_value) == 4
    assert all(len(key) == 3 for key in received_value.keys())
    assert all(50 <= val <= 100 for val in received_value.values())


def test_nested_collections():
    """Generate nested collection structures."""
    received_value = None

    @autosource(
        seed=42,
        data__size=3,
        data__min_value=1,
        data__max_value=10
    )
    def test_func(data: List[List[int]]):
        nonlocal received_value
        received_value = data

    test_func()

    print(f"Generated nested list: {received_value}")
    assert isinstance(received_value, list)
    assert len(received_value) == 3
    assert all(isinstance(inner, list) for inner in received_value)
    assert all(isinstance(val, int) for inner in received_value for val in inner)


if __name__ == '__main__':
    print("=== List of Integers ===")
    test_list_of_integers()

    print("\n=== List with Element Constraints ===")
    test_list_with_element_constraints()

    print("\n=== List of Strings ===")
    test_list_of_strings()

    print("\n=== Set of Strings ===")
    test_set_of_strings()

    print("\n=== Dict Basic ===")
    test_dict_basic()

    print("\n=== Dict with Value Constraints ===")
    test_dict_with_value_constraints()

    print("\n=== Nested Collections ===")
    test_nested_collections()

    print("\n✓ All collection examples passed!")
