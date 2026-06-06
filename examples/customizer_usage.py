"""Customizer usage examples for autoparameterized."""

from autoparameterized import autosource
from autoparameterized.customizers import (
    ChainCustomizer,
    LengthCustomizer,
    NonEmptyCustomizer,
    RangeCustomizer,
    TransformCustomizer,
    TypeCastCustomizer,
)


def test_range_customizer():
    """Use RangeCustomizer to clamp numeric values."""
    from autoparameterized.resolver import create_resolver

    resolver = create_resolver()
    generator = resolver.resolve(int, constraints={'min_value': 0, 'max_value': 200}, seed=42)

    customizer = RangeCustomizer(min_value=50, max_value=150)
    value = generator.generate()
    customized = customizer.customize(value)

    print(f"Original value: {value}, Customized: {customized}")
    assert 50 <= customized <= 150


def test_length_customizer():
    """Use LengthCustomizer to adjust string length."""
    from autoparameterized.resolver import create_resolver

    resolver = create_resolver()
    generator = resolver.resolve(str, seed=42)

    customizer = LengthCustomizer(length=5)
    value = generator.generate()
    customized = customizer.customize(value)

    print(f"Original: '{value}' (len={len(value)}), Customized: '{customized}' (len={len(customized)})")
    assert len(customized) == 5


def test_non_empty_customizer():
    """Use NonEmptyCustomizer to replace empty values."""
    customizer = NonEmptyCustomizer(default_string="default")

    empty_string = ""
    result = customizer.customize(empty_string)

    print(f"Empty string replaced with: '{result}'")
    assert result == "default"


def test_transform_customizer():
    """Use TransformCustomizer to apply transformations."""
    from autoparameterized.resolver import create_resolver

    resolver = create_resolver()
    generator = resolver.resolve(str, constraints={'length': 10}, seed=42)

    customizer = TransformCustomizer(transform='upper')
    value = generator.generate()
    customized = customizer.customize(value)

    print(f"Original: '{value}', Uppercase: '{customized}'")
    assert customized == value.upper()


def test_transform_with_callable():
    """Use TransformCustomizer with a custom function."""
    from autoparameterized.resolver import create_resolver

    resolver = create_resolver()
    generator = resolver.resolve(int, constraints={'min_value': 1, 'max_value': 10}, seed=42)

    customizer = TransformCustomizer(transform=lambda x: x * 2)
    value = generator.generate()
    customized = customizer.customize(value)

    print(f"Original: {value}, Doubled: {customized}")
    assert customized == value * 2


def test_type_cast_customizer():
    """Use TypeCastCustomizer to convert types."""
    customizer = TypeCastCustomizer(target_type=str)

    number = 42
    result = customizer.customize(number)

    print(f"Converted {number} ({type(number).__name__}) to '{result}' ({type(result).__name__})")
    assert result == "42"
    assert isinstance(result, str)


def test_chain_customizer():
    """Use ChainCustomizer to apply multiple customizations in sequence."""
    from autoparameterized.resolver import create_resolver

    resolver = create_resolver()
    generator = resolver.resolve(int, constraints={'min_value': 10, 'max_value': 200}, seed=42)

    customizer = ChainCustomizer(
        RangeCustomizer(min_value=50, max_value=150),
        TransformCustomizer(transform=lambda x: x * 2),
        TypeCastCustomizer(target_type=str),
    )

    value = generator.generate()
    customized = customizer.customize(value)

    print(f"Original: {value}, After chain: '{customized}'")
    assert isinstance(customized, str)
    # Value should be clamped to [50, 150], then doubled, then converted to string
    original_clamped = max(50, min(150, value))
    expected = str(original_clamped * 2)
    assert customized == expected


def test_customizer_with_autosource():
    """Customizers can be integrated into the generation pipeline."""
    # This is a conceptual example showing how customizers work
    # In practice, you'd integrate them into your resolver or generator
    from autoparameterized.resolver import create_resolver

    resolver = create_resolver()

    # Generate a value
    generator = resolver.resolve(str, constraints={'length': 20}, seed=42)
    value = generator.generate()

    # Apply customization
    customizer = ChainCustomizer(
        LengthCustomizer(length=10),
        TransformCustomizer(transform='upper'),
    )
    customized = customizer.customize(value)

    print(f"Generated: '{value}'")
    print(f"Customized: '{customized}'")
    assert len(customized) == 10
    assert customized.isupper()


if __name__ == '__main__':
    print("=== Range Customizer ===")
    test_range_customizer()

    print("\n=== Length Customizer ===")
    test_length_customizer()

    print("\n=== NonEmpty Customizer ===")
    test_non_empty_customizer()

    print("\n=== Transform Customizer ===")
    test_transform_customizer()

    print("\n=== Transform with Callable ===")
    test_transform_with_callable()

    print("\n=== TypeCast Customizer ===")
    test_type_cast_customizer()

    print("\n=== Chain Customizer ===")
    test_chain_customizer()

    print("\n=== Customizer with AutoSource ===")
    test_customizer_with_autosource()

    print("\n✓ All customizer examples passed!")
