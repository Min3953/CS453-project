"""
Core decorator for automatic parameterization.

@autosource decorator automatically generates test parameters from type hints.
- Without count: test runs once with generated values
- With count: test runs N times with different values
"""

from typing import Callable, Optional, get_type_hints


def autosource(
    func: Optional[Callable] = None,
    *,
    count: Optional[int] = None,
    seed: Optional[int] = None,
    **param_constraints
):
    """
    Automatically generate test parameters from type hints.

    Usage:
        # Single execution
        @autosource
        def test_function(age: int, name: str):
            assert age > 0

        # Multiple executions (property-based testing)
        @autosource(count=10, seed=42, age__min_value=18)
        def test_function(age: int):
            assert age >= 18

    Args:
        func: Test function (when used without parentheses)
        count: Number of times to run test (default: 1)
        seed: Random seed for reproducibility
        **param_constraints: Constraints in format param__constraint=value

    Returns:
        Decorated test function
    """

    # Determine if used with or without parentheses
    if func is not None:
        # @autosource (no parentheses) -> single execution
        return _create_wrapper(func, count=1, seed=seed, param_constraints=param_constraints)
    else:
        # @autosource(...) (with parentheses)
        def decorator(f: Callable) -> Callable:
            if count is None:
                # No count specified -> single execution
                return _create_wrapper(f, count=1, seed=seed, param_constraints=param_constraints)
            else:
                # Count specified -> multiple executions
                return _create_wrapper(f, count=count, seed=seed, param_constraints=param_constraints)
        return decorator


def _create_wrapper(func: Callable, count: int, seed: Optional[int], param_constraints: dict):
    """
    Create wrapper that injects generated values.

    Args:
        func: Original test function
        count: Number of executions (1 for single, N for multiple)
        seed: Random seed
        param_constraints: Parameter constraints

    Returns:
        Wrapped function
    """
    # Generate N sets of values and use pytest.mark.parametrize
    try:
        import pytest
    except ImportError:
        raise ImportError(
            "pytest is required for @autosource. "
            "Install with: pip install pytest"
        )

    # Extract type hints
    type_hints = get_type_hints(func)
    param_names = [name for name in type_hints.keys() if name != 'return']

    # If no parameters, handle based on count
    if not param_names:
        if count == 1:
            return func  # No need to do anything
        else:
            return pytest.mark.parametrize('_dummy', range(count))(func)

    # Create resolver once for all type resolution
    from .resolver import create_resolver
    resolver = create_resolver()

    # Register custom generators if specified
    if hasattr(func, '_custom_generators'):
        for type_cls, gen_class in func._custom_generators.items():
            resolver.register(type_cls, gen_class)

    # For count=1, create dual-mode wrapper that supports both direct calls and pytest parametrize
    if count == 1:
        import functools

        @functools.wraps(func)
        def dual_mode_wrapper(*args, **kwargs):
            if args or kwargs:
                # Called with arguments (by pytest parametrize)
                return func(*args, **kwargs)
            else:
                # Called without arguments (direct call) - generate values
                generated_kwargs = {}
                for param_name in param_names:
                    param_type = type_hints[param_name]
                    constraints = _parse_constraints_for_param(param_name, param_constraints)
                    generator = resolver.resolve(param_type, constraints, seed)
                    generated_kwargs[param_name] = generator.generate()
                return func(**generated_kwargs)

        # Generate one test case for pytest
        values = []
        for param_name in param_names:
            param_type = type_hints[param_name]
            constraints = _parse_constraints_for_param(param_name, param_constraints)
            generator = resolver.resolve(param_type, constraints, seed)
            values.append(generator.generate())
        test_cases = [tuple(values) if len(values) > 1 else values[0]]

        # Apply parametrize to the dual-mode wrapper
        return pytest.mark.parametrize(','.join(param_names), test_cases)(dual_mode_wrapper)
    else:
        # For count > 1, generate N test cases
        test_cases = []
        for i in range(count):
            effective_seed = seed + i if seed is not None else None
            values = []
            for param_name in param_names:
                param_type = type_hints[param_name]
                constraints = _parse_constraints_for_param(param_name, param_constraints)
                generator = resolver.resolve(param_type, constraints, effective_seed)
                values.append(generator.generate())
            test_cases.append(tuple(values) if len(values) > 1 else values[0])

        # Apply pytest.mark.parametrize
        return pytest.mark.parametrize(','.join(param_names), test_cases)(func)


# ============================================================================
# Helper functions
# ============================================================================

def _parse_constraints_for_param(param_name: str, param_constraints: dict) -> dict:
    """
    Parse constraints for a specific parameter.

    Extracts constraints in format: param__constraint -> constraint

    Args:
        param_name: Name of the parameter
        param_constraints: All constraints dict

    Returns:
        Dict of constraints for this parameter
    """
    constraints = {}
    prefix = f"{param_name}__"

    for key, value in param_constraints.items():
        if key.startswith(prefix):
            constraint_name = key[len(prefix):]
            constraints[constraint_name] = value

    return constraints


# ============================================================================
# Registry system
# ============================================================================

def register_generator(target_type, generator_class):
    """
    Decorator to register a custom generator for a specific test.

    This decorator allows overriding the default generator for a type
    within a specific test function. Multiple decorators can be stacked
    to override multiple types.

    Important: Must be placed BELOW @autosource decorator (runs first).

    Usage:
        @autosource
        @register_generator(int, CustomIntGenerator)
        def test_function(value: int):
            pass

        # Multiple custom generators
        @autosource
        @register_generator(int, CustomIntGenerator)
        @register_generator(str, CustomStrGenerator)
        def test_function(a: int, b: str):
            pass

    Args:
        target_type: The type to override (e.g., int, str)
        generator_class: The custom generator class to use

    Returns:
        Decorator function
    """
    def decorator(func):
        if not hasattr(func, '_custom_generators'):
            func._custom_generators = {}
        func._custom_generators[target_type] = generator_class
        return func
    return decorator


# ============================================================================
# Helper decorators
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
    def decorator(func):
        if not hasattr(func, '_customizers'):
            func._customizers = {}
        func._customizers[param_name] = customizer
        return func
    return decorator


def freeze_param(param_name: str, value):
    """
    Fix a parameter to a constant value across all test cases.

    Usage:
        @freeze_param('multiplier', 10)
        @autosource(count=5)
        def test_function(value: int, multiplier: int):
            pass
    """
    def decorator(func):
        if not hasattr(func, '_frozen_params'):
            func._frozen_params = {}
        func._frozen_params[param_name] = value
        return func
    return decorator
