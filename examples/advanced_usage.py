"""Advanced usage examples for autoparameterized."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, TypedDict

from autoparameterized import autosource


@dataclass
class Product:
    """Product dataclass."""
    product_id: str
    name: str
    price: float
    stock: int


@dataclass
class OrderItem:
    """Order item with product reference."""
    product: Product
    quantity: int


@dataclass
class Order:
    """Complete order structure."""
    order_id: str
    items: List[OrderItem]
    created_at: datetime
    total: float


class ReviewInfo(TypedDict):
    """Review information."""
    reviewer_id: str
    rating: int
    comment: str
    verified: bool


def test_complex_nested_structure():
    """Generate a complex nested structure with multiple levels."""
    received_value = None

    @autosource(
        seed=42,
        order__order_id__length=12,
        order__items__size=3,
        order__items__product__name__length=20,
        order__items__product__price__min_value=10.0,
        order__items__product__price__max_value=1000.0,
        order__items__quantity__min_value=1,
        order__items__quantity__max_value=10,
        order__total__min_value=30.0,
        order__total__max_value=3000.0
    )
    def test_func(order: Order):
        nonlocal received_value
        received_value = order

    test_func()

    print(f"Generated Order:")
    print(f"  ID: {received_value.order_id}")
    print(f"  Items count: {len(received_value.items)}")
    print(f"  Total: ${received_value.total:.2f}")
    print(f"  Created: {received_value.created_at}")

    for i, item in enumerate(received_value.items, 1):
        print(f"  Item {i}: {item.product.name} x{item.quantity} @ ${item.product.price:.2f}")

    assert isinstance(received_value, Order)
    assert len(received_value.order_id) == 12
    assert len(received_value.items) == 3
    assert all(isinstance(item, OrderItem) for item in received_value.items)
    assert all(10.0 <= item.product.price <= 1000.0 for item in received_value.items)
    assert all(1 <= item.quantity <= 10 for item in received_value.items)


def test_mixed_types_with_complex_constraints():
    """Generate multiple parameters with various complex constraints."""
    received_values = {}

    @autosource(
        seed=42,
        product__name__length=15,
        product__price__min_value=50.0,
        product__price__max_value=500.0,
        reviews__size=5,
        reviews__rating__min_value=1,
        reviews__rating__max_value=5,
        reviews__comment__length=50,
        inventory__size=3,
        inventory__key_length=6
    )
    def test_func(
        product: Product,
        reviews: List[ReviewInfo],
        inventory: Dict[str, int]
    ):
        nonlocal received_values
        received_values = {
            'product': product,
            'reviews': reviews,
            'inventory': inventory
        }

    test_func()

    print(f"Generated Product: {received_values['product'].name} @ ${received_values['product'].price:.2f}")
    print(f"Reviews count: {len(received_values['reviews'])}")
    print(f"Inventory locations: {list(received_values['inventory'].keys())}")

    assert len(received_values['product'].name) == 15
    assert 50.0 <= received_values['product'].price <= 500.0
    assert len(received_values['reviews']) == 5
    assert all(1 <= review['rating'] <= 5 for review in received_values['reviews'])
    assert len(received_values['inventory']) == 3


def test_reproducibility_with_seed():
    """Demonstrate that same seed produces same values."""
    results = []

    @autosource(seed=12345, product__name__length=10)
    def test_func(product: Product):
        results.append(product)

    # Generate twice with same seed
    test_func()
    test_func()

    print(f"First generation:  {results[0]}")
    print(f"Second generation: {results[1]}")

    # They should be identical
    assert results[0].product_id == results[1].product_id
    assert results[0].name == results[1].name
    assert results[0].price == results[1].price
    assert results[0].stock == results[1].stock


def test_datetime_constraints():
    """Generate datetime values with specific range."""
    received_value = None

    @autosource(
        seed=42,
        timestamp__min_value=datetime(2024, 1, 1),
        timestamp__max_value=datetime(2024, 12, 31)
    )
    def test_func(timestamp: datetime):
        nonlocal received_value
        received_value = timestamp

    test_func()

    print(f"Generated datetime: {received_value}")
    assert datetime(2024, 1, 1) <= received_value <= datetime(2024, 12, 31)


def test_real_world_scenario():
    """Simulate a real-world testing scenario for an e-commerce system."""

    @dataclass
    class Customer:
        customer_id: str
        email: str
        join_date: datetime

    @dataclass
    class Transaction:
        transaction_id: str
        customer: Customer
        order: Order
        payment_method: str
        status: str

    received_value = None

    @autosource(
        seed=42,
        transaction__transaction_id__length=16,
        transaction__customer__email__length=20,
        transaction__order__items__size=2,
        transaction__order__items__product__price__min_value=20.0,
        transaction__order__items__product__price__max_value=200.0,
        transaction__payment_method__length=10,
        transaction__status__length=8
    )
    def test_func(transaction: Transaction):
        nonlocal received_value
        received_value = transaction

    test_func()

    print("Generated Transaction:")
    print(f"  Transaction ID: {received_value.transaction_id}")
    print(f"  Customer: {received_value.customer.email}")
    print(f"  Order ID: {received_value.order.order_id}")
    print(f"  Items: {len(received_value.order.items)}")
    print(f"  Payment: {received_value.payment_method}")
    print(f"  Status: {received_value.status}")

    assert isinstance(received_value, Transaction)
    assert isinstance(received_value.customer, Customer)
    assert isinstance(received_value.order, Order)
    assert len(received_value.transaction_id) == 16
    assert len(received_value.order.items) == 2


if __name__ == '__main__':
    print("=== Complex Nested Structure ===")
    test_complex_nested_structure()

    print("\n=== Mixed Types with Complex Constraints ===")
    test_mixed_types_with_complex_constraints()

    print("\n=== Reproducibility with Seed ===")
    test_reproducibility_with_seed()

    print("\n=== DateTime Constraints ===")
    test_datetime_constraints()

    print("\n=== Real-World Scenario ===")
    test_real_world_scenario()

    print("\n✓ All advanced examples passed!")
