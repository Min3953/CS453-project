"""Dataclass usage examples for autoparameterized."""

from dataclasses import dataclass
from typing import List, Dict

from autoparameterized import autosource


@dataclass
class User:
    """Simple user dataclass."""
    username: str
    age: int
    email: str


@dataclass
class Address:
    """Address dataclass."""
    street: str
    city: str
    zipcode: int


@dataclass
class Customer:
    """Customer with nested dataclass."""
    name: str
    address: Address
    balance: float


@dataclass
class Order:
    """Order with collections."""
    order_id: str
    customer: Customer
    items: List[str]
    metadata: Dict[str, int]


def test_simple_dataclass():
    """Generate a simple dataclass instance."""
    received_value = None

    @autosource(seed=42)
    def test_func(user: User):
        nonlocal received_value
        received_value = user

    test_func()

    print(f"Generated User: {received_value}")
    assert isinstance(received_value, User)
    assert isinstance(received_value.username, str)
    assert isinstance(received_value.age, int)
    assert isinstance(received_value.email, str)


def test_dataclass_with_constraints():
    """Generate a dataclass with field constraints."""
    received_value = None

    @autosource(
        seed=42,
        user__username__length=10,
        user__age__min_value=21,
        user__age__max_value=60
    )
    def test_func(user: User):
        nonlocal received_value
        received_value = user

    test_func()

    print(f"Generated User with constraints: {received_value}")
    assert len(received_value.username) == 10
    assert 21 <= received_value.age <= 60


def test_nested_dataclass():
    """Generate a dataclass with nested structure."""
    received_value = None

    @autosource(
        seed=42,
        customer__name__length=15,
        customer__address__city__length=10,
        customer__address__zipcode__min_value=10000,
        customer__address__zipcode__max_value=99999,
        customer__balance__min_value=0.0,
        customer__balance__max_value=10000.0
    )
    def test_func(customer: Customer):
        nonlocal received_value
        received_value = customer

    test_func()

    print(f"Generated Customer: {received_value}")
    assert isinstance(received_value, Customer)
    assert isinstance(received_value.address, Address)
    assert len(received_value.name) == 15
    assert len(received_value.address.city) == 10
    assert 10000 <= received_value.address.zipcode <= 99999
    assert 0.0 <= received_value.balance <= 10000.0


def test_dataclass_with_collections():
    """Generate a dataclass containing collections."""
    received_value = None

    @autosource(
        seed=42,
        order__order_id__length=8,
        order__customer__name__length=10,
        order__items__size=3,
        order__items__length=15,
        order__metadata__size=2
    )
    def test_func(order: Order):
        nonlocal received_value
        received_value = order

    test_func()

    print(f"Generated Order: {received_value}")
    assert isinstance(received_value, Order)
    assert len(received_value.order_id) == 8
    assert isinstance(received_value.customer, Customer)
    assert len(received_value.items) == 3
    assert all(len(item) == 15 for item in received_value.items)
    assert len(received_value.metadata) == 2


def test_list_of_dataclasses():
    """Generate a list of dataclass instances."""
    received_value = None

    @autosource(
        seed=42,
        users__size=5,
        users__username__length=8,
        users__age__min_value=18
    )
    def test_func(users: List[User]):
        nonlocal received_value
        received_value = users

    test_func()

    print(f"Generated list of Users (count: {len(received_value)}):")
    for user in received_value:
        print(f"  - {user}")

    assert len(received_value) == 5
    assert all(isinstance(user, User) for user in received_value)
    assert all(len(user.username) == 8 for user in received_value)
    assert all(user.age >= 18 for user in received_value)


if __name__ == '__main__':
    print("=== Simple Dataclass ===")
    test_simple_dataclass()

    print("\n=== Dataclass with Constraints ===")
    test_dataclass_with_constraints()

    print("\n=== Nested Dataclass ===")
    test_nested_dataclass()

    print("\n=== Dataclass with Collections ===")
    test_dataclass_with_collections()

    print("\n=== List of Dataclasses ===")
    test_list_of_dataclasses()

    print("\n✓ All dataclass examples passed!")
