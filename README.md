# autoparameterized

Python implementation of automatic test parameter generation using type hints.

## Overview

`autoparameterized` is a Python library that automatically generates test data based on type hints, eliminating the need to manually create test parameters. This allows you to write cleaner, more maintainable tests by focusing on test logic rather than test data setup.

## Features

- **Automatic parameter generation** from type hints
- **Built-in generators** for common types: `int`, `str`, `float`, `bool`, `datetime`, `List`, `Set`, `Dict`, `dataclass`
- **Custom generators** via `@register_generator`
- **Customizers** to transform generated values via `@with_customizer`
- **Constraint support** for fine-grained control over generated values
- **Property-based testing** with `count` parameter

> **⚠️ Important**: This library relies on Python type hints. **Parameters or dataclass fields without type hints default to `str`**. Always specify type hints explicitly for correct value generation.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from typing import List
from autoparameterized.decorator import autosource

@autosource
def test_addition(a: int, b: int):
    result = a + b
    assert result == a + b

@autosource(count=10)  # Run test 10 times with different values
def test_list_operations(numbers: List[int]):
    assert isinstance(numbers, list)
    assert len(numbers) == 3  # default size
```

## Using Constraints

Customize generated values using constraint syntax `param__constraint=value`:

```python
@autosource(
    age__min_value=18,
    age__max_value=65,
    name__length=10
)
def test_user_validation(age: int, name: str):
    assert 18 <= age <= 65
    assert len(name) == 10
```

### Collection Constraints

```python
@autosource(
    numbers__size=5,           # List size
    numbers__min_value=0,      # Element constraint
    numbers__max_value=100     # Element constraint
)
def test_list_processing(numbers: List[int]):
    assert len(numbers) == 5
    assert all(0 <= n <= 100 for n in numbers)
```

## Custom Generators

### Creating a Custom Generator

Implement the `TypeGenerator` interface:

```python
from autoparameterized.base import TypeGenerator

class PositiveEvenGenerator(TypeGenerator):
    def generate(self) -> int:
        import random
        value = random.randint(0, 1_000_000)
        return value - (value % 2)
```

### Using Custom Generators

Use `@register_generator` to override the default generator for a type:

```python
from autoparameterized.decorator import autosource, register_generator

@autosource
@register_generator(int, PositiveEvenGenerator)
def test_even_numbers(value: int):
    assert value >= 0
    assert value % 2 == 0
```

### Multiple Custom Generators

Register multiple generators for different types:

```python
class CustomIntGenerator(TypeGenerator):
    def generate(self) -> int:
        return 42

class CustomStrGenerator(TypeGenerator):
    def generate(self) -> str:
        return "custom"

@autosource
@register_generator(int, CustomIntGenerator)
@register_generator(str, CustomStrGenerator)
def test_multiple_custom_generators(num: int, text: str):
    assert num == 42
    assert text == "custom"
```

### Direct Generator Usage

You can also use generators directly without the decorator:

```python
from autoparameterized.generators import IntGenerator, ListGenerator

# Simple generator
int_gen = IntGenerator(constraints={'min_value': 0, 'max_value': 100})
value = int_gen.generate()

# Collection generator with nested constraints
list_gen = ListGenerator(constraints={
    'element_type': int,
    'size': 5,
    'element_constraints': {'min_value': 0, 'max_value': 10}
})
numbers = list_gen.generate()
```

## Customizers

Customizers transform generated values after generation.

### Creating a Customizer

Implement the `Customizer` interface:

```python
from autoparameterized.base import Customizer

class DoubleCustomizer(Customizer):
    def customize(self, value):
        return value * 2

class UpperCaseCustomizer(Customizer):
    def customize(self, value):
        return value.upper()
```

### Using Customizers

Use `@with_customizer` to apply transformations:

```python
from autoparameterized.decorator import autosource, with_customizer

@autosource(value__min_value=1, value__max_value=10)
@with_customizer('value', DoubleCustomizer())
def test_doubled_values(value: int):
    # Original: 1-10, After doubling: 2-20
    assert 2 <= value <= 20
    assert value % 2 == 0
```

### Multiple Customizers

Apply different customizers to different parameters:

```python
@autosource(age__min_value=10, age__max_value=20, name__length=5)
@with_customizer('age', DoubleCustomizer())
@with_customizer('name', UpperCaseCustomizer())
def test_multiple_customizers(age: int, name: str):
    assert 20 <= age <= 40  # doubled
    assert name.isupper()
```

### Customizers with Collections

Customizers automatically apply to each element in collections:

```python
@autosource(numbers__size=3, numbers__min_value=1, numbers__max_value=10)
@with_customizer('numbers', DoubleCustomizer())
def test_list_customization(numbers: List[int]):
    # Each element is doubled
    assert all(2 <= n <= 20 for n in numbers)
```

### Direct Customizer Usage

Apply customizers manually:

```python
from autoparameterized.generators import RangeCustomizer

customizer = RangeCustomizer(min_value=0, max_value=100)
value = customizer.customize(150)  # Returns 100 (clamped)
```

## Supported Types

- **Primitives**: `int`, `str`, `float`, `bool`, `datetime`
- **Collections**: `List[T]`, `Set[T]`, `Dict[K, V]`
- **Complex**: `dataclass` types
- **Nested**: `List[List[int]]`, `List[dataclass]`, etc.

### Type Hint Behavior

**Missing type hints default to `str`:**

```python
from dataclasses import dataclass

@dataclass
class Example:
    typed_field: int        # ✅ Generates int
    untyped_field           # ⚠️ Generates str (defaults to str)

@autosource
def test_with_types(a: int, b: str):
    # ✅ a is int, b is str
    pass

@autosource
def test_without_types(a, b):
    # ⚠️ Both a and b are str (default)
    pass

# For List/Set without element type
@autosource
def test_untyped_list(items: List):
    # ⚠️ List[str] - elements default to str
    assert all(isinstance(item, str) for item in items)
```

**Always specify type hints explicitly** to ensure correct value generation.

## Built-in Generators

| Type | Default Behavior | Constraints |
|------|------------------|-------------|
| `int` | Random int 0-100 | `min_value`, `max_value` |
| `str` | Random 10-char string | `length`, `charset` |
| `float` | Random float 0.0-100.0 | `min_value`, `max_value` |
| `bool` | Random boolean | `probability` |
| `datetime` | Random datetime 1970-2030 | `min_value`, `max_value`, `start`, `end` |
| `List[T]` | 3 elements of type T | `size`, `element_constraints` |
| `Set[T]` | 3 unique elements of type T | `size`, `element_constraints` |
| `Dict[K,V]` | 3 key-value pairs | `size`, `key_constraints`, `value_constraints` |

## Built-in Customizers

- `RangeCustomizer`: Clamp values to a range
- `LengthCustomizer`: Adjust string/list length
- `TransformCustomizer`: Apply transformations (upper, lower, etc.)
- `NonEmptyCustomizer`: Ensure non-empty collections/strings
- `TypeCastCustomizer`: Convert between types
- `RegexStringCustomizer`: Match regex patterns

## Advanced Usage

### Property-Based Testing

Run tests multiple times with different random values:

```python
@autosource(count=100, seed=42)  # Reproducible with seed
def test_property(x: int, y: int):
    # Test runs 100 times with different (x, y) pairs
    assert x + y == y + x  # commutative property
```

### Nested Collections

```python
@autosource
def test_nested_structures(matrix: List[List[int]]):
    assert isinstance(matrix, list)
    assert all(isinstance(row, list) for row in matrix)
    assert all(isinstance(val, int) for row in matrix for val in row)
```

### Dataclass Generation

```python
from dataclasses import dataclass
from typing import List

@dataclass
class User:
    name: str
    age: int
    emails: List[str]

@autosource
def test_user_creation(user: User):
    assert isinstance(user, User)
    assert isinstance(user.name, str)
    assert isinstance(user.age, int)
    assert isinstance(user.emails, list)
```


### Domain-Driven Test Data

Express business domain concepts using Ubiquitous Language in your test data generators:

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional
from autoparameterized.base import TypeGenerator
from autoparameterized.decorator import autosource, register_generator

@dataclass
class DailyBudget:
    date: date
    budget_amount: Optional[float]
    spending_amount: float

class DailyBudgetGenerator(TypeGenerator):
    """Generate daily budgets with positive amounts."""
    def generate(self) -> DailyBudget:
        import random
        from datetime import date, timedelta
        
        base_date = date(2024, 1, 1)
        random_date = base_date + timedelta(days=random.randint(0, 365))
        
        return DailyBudget(
            date=random_date,
            budget_amount=random.uniform(100, 1000),
            spending_amount=random.uniform(0, 500)
        )

class ExhaustedBudgetGenerator(TypeGenerator):
    """Generate budgets where spending exceeds the limit."""
    def generate(self) -> DailyBudget:
        import random
        from datetime import date, timedelta
        
        base_date = date(2024, 1, 1)
        random_date = base_date + timedelta(days=random.randint(0, 365))
        budget = random.uniform(100, 500)
        
        return DailyBudget(
            date=random_date,
            budget_amount=budget,
            spending_amount=budget + random.uniform(1, 200)  # Over budget!
        )

class SufficientBudgetGenerator(TypeGenerator):
    """Generate budgets with remaining balance."""
    def generate(self) -> DailyBudget:
        import random
        from datetime import date, timedelta
        
        base_date = date(2024, 1, 1)
        random_date = base_date + timedelta(days=random.randint(0, 365))
        budget = random.uniform(500, 1000)
        
        return DailyBudget(
            date=random_date,
            budget_amount=budget,
            spending_amount=random.uniform(0, budget - 1)  # Under budget
        )

class UnlimitedBudgetGenerator(TypeGenerator):
    """Generate budgets with no spending limit."""
    def generate(self) -> DailyBudget:
        import random
        from datetime import date, timedelta
        
        base_date = date(2024, 1, 1)
        random_date = base_date + timedelta(days=random.randint(0, 365))
        
        return DailyBudget(
            date=random_date,
            budget_amount=None,  # Unlimited!
            spending_amount=random.uniform(0, 10000)
        )

# Use domain-specific generators in tests
@autosource
@register_generator(DailyBudget, ExhaustedBudgetGenerator)
def test_alert_for_exhausted_budget(budget: DailyBudget):
    # Test reads like business logic
    assert budget.spending_amount > budget.budget_amount
    # alert_system.should_alert(budget) == True

@autosource
@register_generator(DailyBudget, SufficientBudgetGenerator)
def test_no_alert_for_sufficient_budget(budget: DailyBudget):
    assert budget.spending_amount < budget.budget_amount
    # alert_system.should_alert(budget) == False

@autosource
@register_generator(DailyBudget, UnlimitedBudgetGenerator)
def test_unlimited_budget_never_exhausted(budget: DailyBudget):
    assert budget.budget_amount is None
    # budget.is_unlimited() == True
```

This approach makes tests self-documenting and aligns test data with business language.
