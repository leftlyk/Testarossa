import pytest
from source_files.maths_utils import add, subtract, multiply, divide, factorial, is_prime

# Test cases for add(a, b) function
def test_add_normal():
    assert add(2, 3) == 5

def test_add_edge():
    assert add(0, 5) == 5
    
def test_add_error():
    with pytest.raises(TypeError):
        add("2", 3)

# Test cases for subtract(a, b) function
def test_subtract_normal():
    assert subtract(5, 2) == 3

def test_subtract_edge():
    assert subtract(5, 0) == 5
    
def test_subtract_error():
    with pytest.raises(TypeError):
        subtract(5, "2")

# Test cases for multiply(a, b) function
def test_multiply_normal():
    assert multiply(3, 4) == 12

def test_multiply_edge():
    assert multiply(5, 0) == 0
    
def test_multiply_error():
    with pytest.raises(TypeError):
        multiply("3", 4)

# Test cases for divide(a, b) function
def test_divide_normal():
    assert divide(10, 2) == 5

def test_divide_edge():
    assert divide(10, 1) == 10
    
def test_divide_error():
    with pytest.raises(ValueError):
        divide(10, 0)

# Test cases for factorial(n) function
def test_factorial_normal():
    assert factorial(5) == 120

def test_factorial_edge():
    assert factorial(0) == 1
    
def test_factorial_error():
    with pytest.raises(ValueError):
        factorial(-5)

# Test cases for is_prime(n) function
def test_is_prime_normal():
    assert is_prime(7) == True

def test_is_prime_edge():
    assert is_prime(0) == False
    assert is_prime(1) == False
    
def test_is_prime_error():
    assert is_prime(-4) == False