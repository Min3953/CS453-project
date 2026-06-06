"""Basic usage examples for autoparameterized."""

from autoparameterized import autosource


def test_basic_integer():
    """Generate a single integer value."""
    received_value = None

    @autosource(seed=42)
    def test_func(value: int):
        nonlocal received_value
        received_value = value

    test_func()

    print(f"Generated integer: {received_value}")
    assert isinstance(received_value, int)
    assert 0 <= received_value <= 100


def test_integer_with_constraints():
    """Generate an integer with custom constraints."""
    received_value = None

    @autosource(seed=42, value__min_value=10, value__max_value=50)
    def test_func(value: int):
        nonlocal received_value
        received_value = value

    test_func()

    print(f"Generated integer with constraints: {received_value}")
    assert 10 <= received_value <= 50


def test_multiple_parameters():
    """Generate multiple parameters at once."""
    received_values = {}

    @autosource(seed=42, age__min_value=18, age__max_value=65)
    def test_func(name: str, age: int, active: bool):
        nonlocal received_values
        received_values = {'name': name, 'age': age, 'active': active}

    test_func()

    print(f"Generated values: {received_values}")
    assert isinstance(received_values['name'], str)
    assert 18 <= received_values['age'] <= 65
    assert isinstance(received_values['active'], bool)


def test_string_with_length():
    """Generate a string with specific length."""
    received_value = None

    @autosource(seed=42, username__length=8)
    def test_func(username: str):
        nonlocal received_value
        received_value = username

    test_func()

    print(f"Generated username: {received_value}")
    assert len(received_value) == 8


def test_float_with_range():
    """Generate a float with specific range."""
    received_value = None

    @autosource(seed=42, price__min_value=9.99, price__max_value=99.99)
    def test_func(price: float):
        nonlocal received_value
        received_value = price

    test_func()

    print(f"Generated price: {received_value}")
    assert 9.99 <= received_value <= 99.99


def test_bool_with_probability():
    """Generate a boolean with custom probability."""
    true_count = 0
    iterations = 100

    @autosource(value__probability=0.7)
    def test_func(value: bool):
        nonlocal true_count
        if value:
            true_count += 1

    for _ in range(iterations):
        test_func()

    print(f"True count in {iterations} iterations: {true_count}")
    # With probability 0.7, expect around 70% true values
    assert 50 < true_count < 90


if __name__ == '__main__':
    print("=== Basic Integer ===")
    test_basic_integer()

    print("\n=== Integer with Constraints ===")
    test_integer_with_constraints()

    print("\n=== Multiple Parameters ===")
    test_multiple_parameters()

    print("\n=== String with Length ===")
    test_string_with_length()

    print("\n=== Float with Range ===")
    test_float_with_range()

    print("\n=== Bool with Probability ===")
    test_bool_with_probability()

    print("\n✓ All basic examples passed!")
