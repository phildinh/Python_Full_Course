import pytest
from calculator import add, divide, clean_amount, multiply

# ---- add() tests ----

def test_add_two_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 0) == 0

# ---- divide() tests ----

def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

# ---- clean_amount() tests ----

def test_clean_amount_with_dollar_sign():
    assert clean_amount("$1200.50") == 1200.50

def test_clean_amount_with_comma():
    assert clean_amount("$1,200.50") == 1200.50

def test_clean_amount_invalid_input():
    with pytest.raises((ValueError, AttributeError)):
        clean_amount(1200)

# ---- multiply() tests ----
def test_multiply_two_positive_numbers():
    assert multiply(2, 3) == 6

def test_multiply_two_negative_numbers():
    assert multiply(-1, -1) == 1

def test_multiply_by_zero():
    assert multiply(0, 0) == 0