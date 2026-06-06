"""TypedDict usage examples for autoparameterized."""

from typing import TypedDict

from autoparameterized import autosource


class UserProfile(TypedDict):
    """User profile structure."""
    username: str
    age: int
    email: str
    active: bool


class ProductInfo(TypedDict):
    """Product information structure."""
    name: str
    price: float
    stock: int
    available: bool


def test_typed_dict_basic():
    """Generate a TypedDict with default constraints."""
    received_value = None

    @autosource(seed=42)
    def test_func(user: UserProfile):
        nonlocal received_value
        received_value = user

    test_func()

    print(f"Generated UserProfile: {received_value}")
    assert set(received_value.keys()) == {'username', 'age', 'email', 'active'}
    assert isinstance(received_value['username'], str)
    assert isinstance(received_value['age'], int)
    assert isinstance(received_value['email'], str)
    assert isinstance(received_value['active'], bool)


def test_typed_dict_with_constraints():
    """Generate a TypedDict with field-specific constraints."""
    received_value = None

    @autosource(
        seed=42,
        user__username__length=8,
        user__age__min_value=18,
        user__age__max_value=65
    )
    def test_func(user: UserProfile):
        nonlocal received_value
        received_value = user

    test_func()

    print(f"Generated UserProfile with constraints: {received_value}")
    assert len(received_value['username']) == 8
    assert 18 <= received_value['age'] <= 65


def test_typed_dict_product():
    """Generate a product TypedDict with business constraints."""
    received_value = None

    @autosource(
        seed=42,
        product__name__length=20,
        product__price__min_value=0.99,
        product__price__max_value=999.99,
        product__stock__min_value=0,
        product__stock__max_value=1000
    )
    def test_func(product: ProductInfo):
        nonlocal received_value
        received_value = product

    test_func()

    print(f"Generated ProductInfo: {received_value}")
    assert len(received_value['name']) == 20
    assert 0.99 <= received_value['price'] <= 999.99
    assert 0 <= received_value['stock'] <= 1000
    assert isinstance(received_value['available'], bool)


def test_multiple_typed_dicts():
    """Generate multiple TypedDict parameters."""
    received_values = {}

    @autosource(
        seed=42,
        user__username__length=6,
        product__name__length=10
    )
    def test_func(user: UserProfile, product: ProductInfo):
        nonlocal received_values
        received_values = {'user': user, 'product': product}

    test_func()

    print(f"Generated user: {received_values['user']}")
    print(f"Generated product: {received_values['product']}")
    assert len(received_values['user']['username']) == 6
    assert len(received_values['product']['name']) == 10


if __name__ == '__main__':
    print("=== TypedDict Basic ===")
    test_typed_dict_basic()

    print("\n=== TypedDict with Constraints ===")
    test_typed_dict_with_constraints()

    print("\n=== TypedDict Product ===")
    test_typed_dict_product()

    print("\n=== Multiple TypedDicts ===")
    test_multiple_typed_dicts()

    print("\n✓ All TypedDict examples passed!")
