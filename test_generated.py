import pytest
from code_under_test import add, divide

# Test cases for the add function
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_zero():
    assert add(0, 0) == 0
    assert add(0, 5) == 5
    assert add(5, 0) == 5

def test_add_floats():
    assert add(2.5, 3.5) == 6.0

def test_add_large_numbers():
    assert add(1e10, 1e10) == 2e10

# Edge case for add function
def test_add_edge_case():
    assert add(float('inf'), 1) == float('inf')
    assert add(float('-inf'), -1) == float('-inf')

# Test cases for the divide function
def test_divide_positive_numbers():
    assert divide(10, 2) == 5

def test_divide_negative_numbers():
    assert divide(-10, -2) == 5
    assert divide(-10, 2) == -5

def test_divide_zero_numerator():
    assert divide(0, 5) == 0

def test_divide_floats():
    assert divide(7.5, 2.5) == 3.0

def test_divide_large_numbers():
    assert divide(1e10, 1e5) == 100000.0

# Edge case for divide function
def test_divide_edge_case():
    assert divide(float('inf'), 1) == float('inf')
    assert divide(float('-inf'), -1) == float('inf')

# Negative tests for divide function
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_zero_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(0, 0)

# Exception handling tests
def test_divide_non_numeric():
    with pytest.raises(TypeError):
        divide("10", 2)
    with pytest.raises(TypeError):
        divide(10, "2")

# Boundary tests
def test_divide_boundary_values():
    assert divide(1, 1) == 1
    assert divide(1, -1) == -1
    assert divide(-1, 1) == -1
    assert divide(-1, -1) == 1