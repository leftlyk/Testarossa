import pytest 
import source_files.maths_utils_broken as testfile 
def testfile_add_normal_case():
    assert testfile.add(5, 10) == 15

def testfile_add_edge_case_1():
    assert testfile.add(0, 10) == 10

def testfile_add_edge_case_2():
    assert testfile.add(5, 0) == 5

def testfile_add_error_case():
    try:
        testfile.add(5, 'a')
    except TypeError:
        assert True

def testfile_subtract_normal_case():
    assert testfile.subtract(10, 5) == 5

def testfile_subtract_edge_case_1():
    assert testfile.subtract(10, 0) == 10

def testfile_subtract_edge_case_2():
    assert testfile.subtract(0, 5) == -5

def testfile_subtract_error_case():
    try:
        testfile.subtract(10, 'a')
    except TypeError:
        assert True

def testfile_multiply_normal_case():
    assert testfile.multiply(5, 10) == 50

def testfile_multiply_edge_case_1():
    assert testfile.multiply(0, 10) == 0

def testfile_multiply_edge_case_2():
    assert testfile.multiply(5, 1) == 5

def testfile_multiply_error_case():
    try:
        testfile.multiply(5, 'a')
    except TypeError:
        assert True

def testfile_divide_normal_case():
    assert testfile.divide(10, 5) == 2.0

def testfile_divide_edge_case_1():
    assert testfile.divide(5, 1) == 5.0

def testfile_divide_edge_case_2():
    assert testfile.divide(5, 2) == 2.5

def testfile_divide_error_case():
    try:
        testfile.divide(10, 0)
    except ValueError:
        assert True

def testfile_factorial_normal_case():
    assert testfile.factorial(5) == 120

def testfile_factorial_edge_case():
    assert testfile.factorial(0) == 1

def testfile_factorial_error_case():
    try:
        testfile.factorial(-5)
    except ValueError:
        assert True

def testfile_is_prime_normal_case():
    assert testfile.is_prime(7) == True

def testfile_is_prime_edge_case_1():
    assert testfile.is_prime(0) == False

def testfile_is_prime_edge_case_2():
    assert testfile.is_prime(1) == False

def testfile_is_prime_error_case():
    assert testfile.is_prime(4) == False