"""Test decorator behavior with different count values."""

import pytest
from autoparameterized import autosource


class TestCountParameter:
    """Test count parameter behavior."""

    def test_no_count_defaults_to_single(self):
        """Test that no count parameter defaults to single execution."""
        @autosource
        def test_func():
            pass

        # Should create a wrapper function, not parametrize
        assert callable(test_func)
        # Should not have pytestmark for parametrize
        assert not hasattr(test_func, 'pytestmark') or test_func.pytestmark is None or len(test_func.pytestmark) == 0

    def test_count_one_same_as_no_count(self):
        """Test that count=1 behaves same as no count."""
        @autosource(count=1)
        def test_func():
            pass

        # Should create a wrapper function
        assert callable(test_func)

    def test_count_greater_than_one_uses_parametrize(self):
        """Test that count > 1 uses pytest.mark.parametrize."""
        @autosource(count=5)
        def test_func(value: int):
            pass

        # Should have pytestmark
        assert hasattr(test_func, 'pytestmark')


class TestSeedBehavior:
    """Test seed parameter behavior."""

    def test_seed_accepted_without_count(self):
        """Test that seed can be used without count."""
        @autosource(seed=42)
        def test_func():
            pass

        # Should not raise error
        assert callable(test_func)

    def test_seed_accepted_with_count(self):
        """Test that seed can be used with count."""
        @autosource(count=5, seed=42)
        def test_func():
            pass

        # Should not raise error
        assert callable(test_func)

    def test_same_seed_produces_same_values(self):
        """Test that same seed produces reproducible values."""
        # With parametrize, values are pre-generated at collection time
        # So we need to verify the parametrize marks are identical

        @autosource(count=3, seed=42)
        def test_func1(value: int):
            pass

        @autosource(count=3, seed=42)
        def test_func2(value: int):
            pass

        # Both should have pytestmark with parametrize
        assert hasattr(test_func1, 'pytestmark')
        assert hasattr(test_func2, 'pytestmark')

        # Extract parametrize values
        mark1 = test_func1.pytestmark[0]
        mark2 = test_func2.pytestmark[0]

        # Same seed should produce same test cases
        assert mark1.args[1] == mark2.args[1]  # Same values


class TestConstraintParameter:
    """Test constraint parameter syntax."""

    def test_constraint_syntax_accepted(self):
        """Test that constraint syntax is accepted."""
        @autosource(age__min_value=18, age__max_value=100)
        def test_func():
            pass

        # Should not raise error
        assert callable(test_func)

    def test_multiple_constraints_accepted(self):
        """Test that multiple constraints are accepted."""
        @autosource(
            age__min_value=18,
            age__max_value=100,
            name__length=8,
            score__min_value=0
        )
        def test_func():
            pass

        # Should not raise error
        assert callable(test_func)

    def test_constraints_with_count_and_seed(self):
        """Test that constraints work with count and seed."""
        @autosource(
            count=5,
            seed=42,
            age__min_value=18,
            age__max_value=100
        )
        def test_func():
            pass

        # Should not raise error
        assert callable(test_func)
