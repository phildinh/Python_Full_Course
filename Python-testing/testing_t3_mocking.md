# Mocking API Calls — Study Notes (T3)

> **Purpose:** Quick recap of how to test API-dependent functions without making real HTTP requests.

---

## Why mocking matters

You've built a function that calls a real API. Testing it by hitting the real API is:

- **Slow** — every test run makes a real HTTP request
- **Unreliable** — if the API is down, your tests fail even though your code is fine
- **Expensive** — some APIs charge per call or have rate limits

**Mocking** replaces the real API call with a fake one that returns data you control. Your function doesn't know the difference.

---

## The analogy

A mock is like a stunt double in a movie. The director doesn't send the real actor into a burning building — they send a stunt double who behaves exactly like the actor for that scene. Your test doesn't call the real API — it uses a mock that behaves exactly like the API for that test.

---

## The two key tools

| Tool | What it does |
|------|-------------|
| `MagicMock()` | Creates a fake object you control completely |
| `patch(...)` | Temporarily replaces a real function with your mock |

```python
from unittest.mock import patch, MagicMock
```

---

## The bad way — calling the real API in tests

```python
def test_get_character():
    result = get_character(1)
    assert result["name"] == "Rick Sanchez"   # breaks if API is down
```

Unreliable, slow, and burns your rate limit on every test run.

---

## The good way — mocking with unittest.mock

```python
from unittest.mock import patch, MagicMock
from api_helpers import get_character

def test_get_character_returns_correct_fields():
    # 1. build the fake response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human"
    }
    mock_response.raise_for_status.return_value = None

    # 2. patch requests.get to return our fake response
    with patch("api_helpers.requests.get", return_value=mock_response):
        result = get_character(1)

    # 3. assert the output
    assert result["id"] == 1
    assert result["name"] == "Rick Sanchez"
    assert result["status"] == "Alive"
```

---

## Three concepts to understand

### MagicMock()

Creates a fake object you control completely. You tell it exactly what to return when its methods are called:

```python
mock_response = MagicMock()
mock_response.json.return_value = {"id": 1, "name": "Rick Sanchez"}  # controls .json()
mock_response.raise_for_status.return_value = None                    # controls .raise_for_status()
```

### patch()

Temporarily replaces a real function with your mock. When the `with` block ends, the real function is restored:

```python
with patch("api_helpers.requests.get", return_value=mock_response):
    result = get_character(1)   # requests.get is now your mock inside here
# requests.get is back to normal here
```

### The patch path rule

**Always patch where it's used, not where it's defined.**

Since `api_helpers.py` imports `requests`, you patch `api_helpers.requests.get` — not `requests.get`.

```python
# wrong
with patch("requests.get", ...):

# right — patch it where it's used
with patch("api_helpers.requests.get", ...):
```

---

## return_value vs side_effect

| | What it does | When to use it |
|-|-------------|----------------|
| `return_value` | Returns a value when the method is called | Normal responses |
| `side_effect` | Raises an exception when the method is called | Simulating errors |

---

## Testing error scenarios

### Bad status code (404, 500) — error on raise_for_status

A response was received but it had a bad status code. The error belongs on `raise_for_status`:

```python
def test_get_character_raises_on_bad_status():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("api_helpers.requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            get_character(999)
```

### No response at all (ConnectionError) — error on requests.get itself

The server was never reached. No response exists. The error belongs on `requests.get`:

```python
def test_get_character_raises_on_connection_error():
    with patch("api_helpers.requests.get", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            get_character(1)
```

---

## The key distinction

| Scenario | Where the error goes |
|----------|---------------------|
| Bad status code (`404`, `500`) | `mock_response.raise_for_status.side_effect` |
| No response at all (`ConnectionError`) | `patch(..., side_effect=...)` on `requests.get` |

---

## Full example — api_helpers.py

```python
import requests

def get_character(character_id):
    """Fetches a single character from the Rick and Morty API"""
    response = requests.get(
        url=f"https://rickandmortyapi.com/api/character/{character_id}",
        timeout=10
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id": data["id"],
        "name": data["name"],
        "status": data["status"]
    }
```

## Full example — test_api_helpers.py

```python
import pytest
import requests
from unittest.mock import patch, MagicMock
from api_helpers import get_character

def test_get_character_returns_correct_fields():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human"
    }
    mock_response.raise_for_status.return_value = None

    with patch("api_helpers.requests.get", return_value=mock_response):
        result = get_character(1)

    assert result["id"] == 1
    assert result["name"] == "Rick Sanchez"
    assert result["status"] == "Alive"

def test_get_character_raises_on_bad_status():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("api_helpers.requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            get_character(999)

def test_get_character_raises_on_connection_error():
    with patch("api_helpers.requests.get", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            get_character(1)
```

---

## Key rules to remember

1. **Never call real APIs in tests** — slow, unreliable, expensive
2. **Patch where it's used, not where it's defined** — `api_helpers.requests.get` not `requests.get`
3. **`return_value` for normal responses, `side_effect` for errors**
4. **ConnectionError goes on `requests.get`** — no response exists, so `raise_for_status` is never reached
5. **HTTPError goes on `raise_for_status`** — a response was received but had a bad status

---

## Quick comprehension check

- Why should you never call a real API in a test?
- You want to simulate a `500` server error. Where does `side_effect` go?
- You want to simulate a network timeout. Where does `side_effect` go?
- What does `patch("api_helpers.requests.get", ...)` do after the `with` block ends?

---

*Next: T4 — Testing pipeline functions (applying mocking to real ETL code)*
