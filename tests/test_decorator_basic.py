"""Test basic decorator functionality."""

import pytest
from autoparameterized import autosource


class TestDecoratorSyntax:
    """Test that decorator can be used with different syntaxes."""

    def test_decorator_without_parentheses(self):
        """Test @autosource without parentheses."""
        @autosource
        def dummy_test():
            pass

        # Should not raise error
        assert callable(dummy_test)

    def test_decorator_with_empty_parentheses(self):
        """Test @autosource() with empty parentheses."""
        @autosource()
        def dummy_test():
            pass

        # Should not raise error
        assert callable(dummy_test)

    def test_decorator_with_seed(self):
        """Test @autosource(seed=42)."""
        @autosource(seed=42)
        def dummy_test():
            pass

        # Should not raise error
        assert callable(dummy_test)

    def test_decorator_with_count(self):
        """Test @autosource(count=5)."""
        @autosource(count=5)
        def dummy_test():
            pass

        # Should not raise error
        assert callable(dummy_test)

    def test_decorator_with_constraints(self):
        """Test @autosource with constraints."""
        @autosource(seed=42, age__min_value=18, age__max_value=100)
        def dummy_test():
            pass

        # Should not raise error
        assert callable(dummy_test)


class TestDecoratorBehavior:
    """Test decorator behavior (these tests require full implementation)."""

    def test_single_execution_injects_values(self):
        """Test that @autosource injects values for single execution."""
        execution_count = 0

        @autosource
        def test_func(value: int):
            nonlocal execution_count
            execution_count += 1
            assert isinstance(value, int)

        test_func()
        assert execution_count == 1

    def test_multiple_execution_with_count(self):
        """Test that @autosource(count=N) creates N test cases."""
        @autosource(count=5, seed=42)
        def test_func(value: int):
            assert isinstance(value, int)

        # Check if pytest.mark.parametrize was applied
        assert hasattr(test_func, 'pytestmark')

    def test_type_hints_processed(self):
        """Test that type hints are extracted and used."""
        @autosource(seed=42)
        def test_func(value: int, text: str):
            assert isinstance(value, int)
            assert isinstance(text, str)

        test_func()


class TestDecoratorMetadata:
    """Test decorator preserves function metadata."""

    def test_preserves_function_name(self):
        """Test that decorator preserves function name."""
        @autosource
        def my_test_function():
            pass

        assert my_test_function.__name__ == 'my_test_function'

    def test_preserves_docstring(self):
        """Test that decorator preserves docstring."""
        @autosource
        def my_test_function():
            """This is a test docstring."""
            pass

        assert my_test_function.__doc__ == """This is a test docstring."""
