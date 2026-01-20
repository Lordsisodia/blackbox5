"""
Comprehensive test suite for the add_numbers function.

Run tests with: pytest test_add_numbers.py -v
Or with coverage: pytest test_add_numbers.py -v --cov=add_numbers --cov-report=html
"""

import pytest
from add_numbers import add_numbers


class TestAddNumbersBasicFunctionality:
    """Test basic addition functionality."""
    
    def test_positive_integers(self):
        """Test adding two positive integers."""
        assert add_numbers(5, 10) == 15
        assert add_numbers(0, 0) == 0
        assert add_numbers(1, 1) == 2
    
    def test_negative_integers(self):
        """Test adding negative integers."""
        assert add_numbers(-5, -10) == -15
        assert add_numbers(-5, 10) == 5
        assert add_numbers(5, -10) == -5
    
    def test_floats(self):
        """Test adding floating point numbers."""
        assert add_numbers(2.5, 3.5) == 6.0
        assert add_numbers(0.1, 0.2) == pytest.approx(0.3)  # Handles floating point precision
        assert add_numbers(-1.5, 2.5) == 1.0
    
    def test_mixed_types(self):
        """Test adding mixed int and float types."""
        assert add_numbers(5, 2.5) == 7.5
        assert add_numbers(2.5, 5) == 7.5
        assert isinstance(add_numbers(5, 2.5), float)
    
    def test_zero(self):
        """Test addition with zero."""
        assert add_numbers(0, 5) == 5
        assert add_numbers(5, 0) == 5
        assert add_numbers(0, 0) == 0


class TestAddNumbersErrorHandling:
    """Test error handling for invalid inputs."""
    
    def test_string_first_argument(self):
        """Test that string as first argument raises TypeError."""
        with pytest.raises(TypeError, match="First argument must be int or float"):
            add_numbers("5", 10)
    
    def test_string_second_argument(self):
        """Test that string as second argument raises TypeError."""
        with pytest.raises(TypeError, match="Second argument must be int or float"):
            add_numbers(5, "10")
    
    def test_both_strings(self):
        """Test that strings as both arguments raises TypeError."""
        with pytest.raises(TypeError, match="First argument must be int or float"):
            add_numbers("5", "10")
    
    def test_none_argument(self):
        """Test that None as argument raises TypeError."""
        with pytest.raises(TypeError, match="First argument must be int or float"):
            add_numbers(None, 10)
    
    def test_list_argument(self):
        """Test that list as argument raises TypeError."""
        with pytest.raises(TypeError, match="First argument must be int or float"):
            add_numbers([1, 2], 10)
    
    def test_boolean_argument(self):
        """Test that boolean is treated as int (Python allows this)."""
        # Note: In Python, bool is a subclass of int, so this is valid
        # True == 1, False == 0
        assert add_numbers(True, 5) == 6  # True + 5
        assert add_numbers(False, 5) == 5  # False + 5


class TestAddNumbersEdgeCases:
    """Test edge cases and special values."""
    
    def test_very_large_numbers(self):
        """Test adding very large numbers."""
        large_num = 10**100
        result = add_numbers(large_num, large_num)
        assert result == 2 * 10**100
    
    def test_very_small_numbers(self):
        """Test adding very small decimal numbers."""
        result = add_numbers(1e-10, 2e-10)
        assert result == pytest.approx(3e-10)
    
    def test_return_type_integers(self):
        """Test that adding two integers returns an integer."""
        result = add_numbers(5, 10)
        assert isinstance(result, int)
    
    def test_return_type_with_float(self):
        """Test that adding with any float returns a float."""
        result1 = add_numbers(5.0, 10)
        result2 = add_numbers(5, 10.0)
        result3 = add_numbers(5.0, 10.0)
        assert isinstance(result1, float)
        assert isinstance(result2, float)
        assert isinstance(result3, float)


class TestAddNumbersDocumentation:
    """Test that the function is properly documented."""
    
    def test_has_docstring(self):
        """Test that the function has a docstring."""
        assert add_numbers.__doc__ is not None
        assert len(add_numbers.__doc__) > 0
    
    def test_docstring_contains_parameters(self):
        """Test that docstring documents parameters."""
        doc = add_numbers.__doc__
        assert "Parameters" in doc or "Args" in doc
        assert "a" in doc
        assert "b" in doc
    
    def test_docstring_contains_returns(self):
        """Test that docstring documents return value."""
        doc = add_numbers.__doc__
        assert "Returns" in doc or "Return" in doc
