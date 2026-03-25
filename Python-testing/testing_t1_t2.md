# Testing Fundamentals — Study Notes (T1 + T2)

> **Purpose:** Quick recap of why testing matters and how to write tests with pytest from scratch.

---

## T1 — Why testing exists

### The business problem

You refactor a small function in your pipeline. It doesn't crash. You deploy it. The next morning your analyst calls — the revenue numbers are wrong. Your change silently dropped cents on 50,000 orders.

**Testing would have caught that in 10 seconds before it ever reached production.**

### The bad way — manual testing

```
change the function → run the script → it doesn't crash → assume it works → deploy
```

No crash does not mean correct. This is the trap most beginners fall into.

### The good way — automated tests

```
write a test that says "given this input, I expect this exact output"
run pytest
if your change breaks the expectation, pytest tells you immediately
before anything touches production
```

### The three questions every test answers

```
1. Given this input...
2. When I run this function...
3. I expect this output
```

Every test you'll ever write follows that structure.

### The full testing cycle

```
write function → write test → tests pass ✅
change function → tests fail ❌ → fix the bug → tests pass ✅
```

The test doesn't change. The expectation doesn't change. The moment your code stops meeting the expectation, pytest tells you immediately.

### Why it matters for your DE career

Every company running data pipelines in production uses automated testing. When an interviewer asks "how do you ensure data quality in your pipelines?" — tests are your answer.

---

## T2 — pytest basics

### Setup

```bash
pip install pytest
```

File structure:
```
testing_practice/
├── calculator.py       ← your functions
└── test_calculator.py  ← your tests
```

### Running tests

```bash
pytest test_calculator.py -v
```

`-v` = verbose — prints each test name and result so you can see exactly what ran.

Output format:
```
test_calculator.py::test_add_two_positive_numbers  PASSED
test_calculator.py::test_divide_by_zero            FAILED
```

`file::function_name` — tells you exactly where to look when something fails.

---

### The three types of inputs you always test

| Type | What it is | Example |
|------|-----------|---------|
| **Happy path** | Normal expected input | `add(2, 3)` → `5` |
| **Edge case** | Boundary or unusual but valid input | `add(0, 0)` → `0` |
| **Bad input** | Input that should raise an error | `divide(10, 0)` → `ValueError` |

> Every function needs at least one test for each type.

---

### Writing a basic test

```python
from calculator import add

def test_add_two_positive_numbers():
    result = add(2, 3)
    assert result == 5
```

Three rules:
- Function name must start with `test_`
- `assert` checks your expectation — if false, the test fails
- Test name should read like a sentence describing what it checks

---

### Naming convention

```
test_{function_name}_{scenario_being_tested}
```

Examples:
- `test_add_two_positive_numbers`
- `test_divide_by_zero_raises_error`
- `test_clean_amount_with_comma`

Good names matter — with 100 tests across 10 files, a clear name tells you exactly what broke without reading the code.

---

### Testing that errors are raised correctly

```python
import pytest

def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

- `pytest.raises(ValueError)` — passes only if `ValueError` is raised. Fails if no error is raised.
- `match="..."` — optionally checks the error message too
- Pass a tuple for multiple acceptable error types: `pytest.raises((ValueError, AttributeError))`

---

### Full example — calculator.py

```python
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def clean_amount(value):
    """Strips $ sign and converts to float — like cleaning order amounts from an API"""
    return float(value.replace("$", "").replace(",", ""))

def multiply(a, b):
    return a * b
```

### Full example — test_calculator.py

```python
import pytest
from calculator import add, divide, clean_amount, multiply

# ---- add() ----
def test_add_two_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 0) == 0

# ---- divide() ----
def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

# ---- clean_amount() ----
def test_clean_amount_with_dollar_sign():
    assert clean_amount("$1200.50") == 1200.50

def test_clean_amount_with_comma():
    assert clean_amount("$1,200.50") == 1200.50

def test_clean_amount_invalid_input():
    with pytest.raises((ValueError, AttributeError)):
        clean_amount(1200)

# ---- multiply() ----
def test_multiply_two_positive_numbers():
    assert multiply(2, 3) == 6

def test_multiply_two_negative_numbers():
    assert multiply(-1, -1) == 1

def test_multiply_by_zero():
    assert multiply(0, 0) == 0
```

---

## Key rules to remember

1. **Test name starts with `test_`** — pytest won't find it otherwise
2. **Name = `test_{function}_{scenario}`** — readable names save debugging time
3. **Three test types per function** — happy path, edge case, bad input
4. **`assert` is your expectation** — if it's false, the test fails loudly
5. **`pytest.raises()`** — use this to test that errors are raised correctly
6. **No crash ≠ correct** — always write explicit assertions

---

## Quick comprehension check

- Your test is named `test_something`. pytest can't find it. What's wrong?
- What's the difference between a happy path test and an edge case test?
- You want to test that `clean_amount(None)` raises an error. How do you write that?
- You change a function and all tests still pass. What does that tell you?

---

*Next: T3 — Mocking API calls (testing without hitting a real API)*
