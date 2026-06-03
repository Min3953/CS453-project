"""
Core decorator for automatic parameterization (SKELETON).

This is a skeleton implementation showing the overall structure.
Team members should complete the TODOs.
"""

from datetime import datetime
from typing import Callable, get_type_hints

from .base import TypeGenerator
from .generators import (
    BoolGenerator,
    DateTimeGenerator,
    FloatGenerator,
    IntGenerator,
    StringGenerator,
)


_GENERATOR_REGISTRY = {
    int: IntGenerator,
    str: StringGenerator,
    float: FloatGenerator,
    bool: BoolGenerator,
    datetime: DateTimeGenerator,
}


def autosource(count: int = 10, seed: int = None, **param_constraints):
    """
    Decorator that automatically generates test parameters from type hints.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility
        **param_constraints: Constraints in format param__constraint=value
            Example: age__min_value=18, age__max_value=65

    Usage:
        @autosource(count=5, seed=42, age__min_value=18, age__max_value=100)
        def test_function(age: int, name: str):
            assert 18 <= age <= 100
            assert isinstance(name, str)

    Implementation steps:
        1. Extract type hints from function
        2. Parse param_constraints to map to each parameter
        3. For each test case (count times):
           - For each parameter:
             - Get appropriate generator for the type
             - Generate value with constraints
        4. Wrap with pytest.mark.parametrize
    """

    def decorator(func: Callable) -> Callable:
        # TODO: Step 1 - Extract type hints
        # Hint: use get_type_hints(func)
        type_hints = get_type_hints(func)

        # TODO: Step 2 - Parse param_constraints
        # Format: "param__constraint" -> {param: {constraint: value}}
        # Example: "age__min_value" -> {'age': {'min_value': ...}}
        constraints_by_param = {}
        # ... parsing logic here ...

        # TODO: Step 3 - Generate test cases
        param_names = []
        param_values = []

        for param_name, param_type in type_hints.items():
            if param_name == 'return':
                continue
            param_names.append(param_name)

        # Generate 'count' test cases
        for i in range(count):
            test_case = []
            case_seed = seed + i if seed is not None else None

            for param_name in param_names:
                param_type = type_hints[param_name]
                constraints = constraints_by_param.get(param_name, {})

                # TODO: Get generator for param_type
                # generator = get_generator_for_type(param_type, constraints, case_seed)
                # value = generator.generate()

                # PLACEHOLDER: For now, just append None
                value = None
                test_case.append(value)

            param_values.append(tuple(test_case) if len(test_case) > 1 else test_case[0])

        # TODO: Step 4 - Wrap with pytest.mark.parametrize
        # import pytest
        # argnames = ','.join(param_names)
        # return pytest.mark.parametrize(argnames, param_values)(func)

        # PLACEHOLDER: Return function unchanged for now
        return func

    return decorator


# ============================================================================
# TODO: Implement helper functions
# ============================================================================

def get_generator_for_type(param_type, constraints: dict, seed: int):
    """
    Map a Python type to its corresponding generator.

    Steps:
        1. Check if type is Optional[T] -> extract T
        2. Check if type is List[T] -> use ListGenerator with element_type
        3. Check if type is a dataclass -> use DataclassGenerator
        4. Check custom registry -> use registered generator
        5. Use built-in generator mapping (int->IntGenerator, etc.)

    Args:
        param_type: The type to generate values for
        constraints: Constraints to pass to generator
        seed: Random seed

    Returns:
        TypeGenerator instance
    """
    generator_class = _GENERATOR_REGISTRY.get(param_type)

    if generator_class is None:
        raise TypeError(f"No generator registered for type: {param_type!r}")

    return generator_class(constraints=constraints, seed=seed)


# ============================================================================
# TODO: Implement registry system
# ============================================================================

def register_generator(target_type):
    """
    Decorator to register a custom generator for a type.

    Usage:
        @register_generator(MyClass)
        class MyClassGenerator(TypeGenerator):
            def generate(self):
                return MyClass(...)
    """
    def decorator(generator_class):
        if not isinstance(generator_class, type) or not issubclass(generator_class, TypeGenerator):
            raise TypeError("generator_class must be a TypeGenerator subclass")

        _GENERATOR_REGISTRY[target_type] = generator_class
        return generator_class
    return decorator


# ============================================================================
# TODO: Implement helper decorators
# ============================================================================

def with_customizer(param_name: str, customizer):
    """
    Attach a customizer to a specific parameter.

    Usage:
        @with_customizer('age', RangeCustomizer(0, 100))
        @autosource(count=5)
        def test_function(age: int):
            pass
    """
    # TODO: Attach customizer to function metadata
    pass


def freeze_param(param_name: str, value):
    """
    Fix a parameter to a constant value across all test cases.

    Usage:
        @freeze_param('multiplier', 10)
        @autosource(count=5)
        def test_function(value: int, multiplier: int):
            pass
    """
    # TODO: Attach frozen value to function metadata
    pass
