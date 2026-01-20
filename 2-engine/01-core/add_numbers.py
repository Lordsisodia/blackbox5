"""
Simple Arithmetic Operations Module

This module provides basic arithmetic operations with proper type safety
and error handling.
"""

from typing import Union


def add_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers together.

    This function takes two numeric values (integers or floats) and returns
    their sum. Both parameters must be of numeric types.

    Parameters
    ----------
    a : Union[int, float]
        The first addend (number to be added)
    b : Union[int, float]
        The second addend (number to be added)

    Returns
    -------
    Union[int, float]
        The sum of the two input numbers. Returns an int if both inputs are ints,
        otherwise returns a float.

    Raises
    ------
    TypeError
        If either `a` or `b` is not an int or float

    Examples
    --------
    >>> add_numbers(2, 3)
    5

    >>> add_numbers(2.5, 3.5)
    6.0

    >>> add_numbers(-1, 1)
    0

    >>> add_numbers(2.5, 3)
    5.5
    """
    # Validate input types
    if not isinstance(a, (int, float)):
        raise TypeError(f"First argument must be int or float, got {type(a).__name__}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Second argument must be int or float, got {type(b).__name__}")

    # Perform addition
    return a + b


if __name__ == "__main__":
    # Usage examples
    print("=== Usage Examples ===")
    
    # Basic integer addition
    result1 = add_numbers(5, 10)
    print(f"add_numbers(5, 10) = {result1}")
    
    # Float addition
    result2 = add_numbers(3.14, 2.86)
    print(f"add_numbers(3.14, 2.86) = {result2}")
    
    # Mixed types
    result3 = add_numbers(5, 2.5)
    print(f"add_numbers(5, 2.5) = {result3}")
    
    # Negative numbers
    result4 = add_numbers(-10, 5)
    print(f"add_numbers(-10, 5) = {result4}")
    
    # Error handling examples (commented out to prevent script failure)
    # Uncomment to see error handling in action
    
    # try:
    #     add_numbers("5", 10)  # TypeError: First argument must be int or float
    # except TypeError as e:
    #     print(f"Error: {e}")
