# Rate Limiting and Retries — Study Notes

> **Purpose:** Quick recap of how to handle rate limits and transient errors gracefully in Python data pipelines.

---

## Why this matters

APIs enforce rate limits — they only allow a certain number of calls per minute to protect their servers. Hit the limit and they shut you out temporarily with a `429`. A server hiccup gives you a `500`.

Both are temporary. Both should trigger a retry — not a crash.

---

## The bad way — no retry logic

```python
response = requests.get(url=..., params=...)
response.raise_for_status()   # crashes on 429 or 500, pipeline dies
```

Your Airflow DAG shows red at 2am and you lose all progress.

---

## The retry strategy — exponential backoff

Don't retry immediately — wait a bit longer each time. This gives the server breathing room.

```
attempt 1 fails → wait 2 seconds  → retry
attempt 2 fails → wait 4 seconds  → retry
attempt 3 fails → wait 8 seconds  → retry
then give up
```

For `429` specifically — always read the `Retry-After` header. The API tells you exactly how long to wait. Respect it.

---

## Retry vs stop — always remember this rule

| Code | Cause | Strategy |
|------|-------|----------|
| `429` | Rate limited | Retry after waiting |
| `5xx` | Server error | Retry with backoff |
| `4xx` | Your fault | Stop — retrying won't fix it |

> A `401` or `404` will never fix itself. Never retry on `4xx` errors.

---

## The production way — tenacity library

```bash
pip install tenacity
```

```python
import requests
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

def wait_for_rate_limit(retry_state):
    exc = retry_state.outcome.exception()
    if hasattr(exc, 'response') and exc.response.status_code == 429:
        wait = int(exc.response.headers.get("Retry-After", 60))
        print(f"Rate limited. Waiting {wait}s...")
        time.sleep(wait)
    else:
        print(f"Retrying after error... attempt {retry_state.attempt_number}")

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=16),
    retry=retry_if_exception_type(requests.exceptions.HTTPError),
    before_sleep=wait_for_rate_limit
)
def get_with_retry(url, params):
    response = requests.get(url=url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
```

---

## What each tenacity parameter does

| Parameter | What it does |
|-----------|-------------|
| `stop_after_attempt(5)` | Give up after 5 tries |
| `wait_exponential(min=2, max=16)` | Wait 2s, 4s, 8s, 16s between attempts |
| `retry_if_exception_type(HTTPError)` | Only retry on HTTP errors |
| `before_sleep=wait_for_rate_limit` | Custom hook — runs between retries |

---

## The full working script — pagination + tenacity

```python
import requests
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

def wait_for_rate_limit(retry_state):
    exc = retry_state.outcome.exception()
    if hasattr(exc, 'response') and exc.response.status_code == 429:
        wait = int(exc.response.headers.get("Retry-After", 60))
        print(f"Rate limited. Waiting {wait}s...")
        time.sleep(wait)
    else:
        print(f"Retrying after error... attempt {retry_state.attempt_number}")

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=16),
    retry=retry_if_exception_type(requests.exceptions.HTTPError),
    before_sleep=wait_for_rate_limit
)
def get_with_retry(url, params):
    response = requests.get(url=url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


all_characters = []
page = 1

while True:
    data = get_with_retry(
        url="https://rickandmortyapi.com/api/character",
        params={"page": page}
    )

    all_characters.extend(data["results"])
    print(f"Fetched page {page} - {len(data['results'])} characters")

    if not data["info"]["next"]:
        break

    page += 1

print(f"Total characters fetched: {len(all_characters)}")
```

---

## The before_sleep hook explained

`before_sleep` is a tenacity hook that runs between retry attempts. It receives a `retry_state` object containing the exception that caused the failure.

```python
def wait_for_rate_limit(retry_state):
    exc = retry_state.outcome.exception()          # get the exception
    if exc.response.status_code == 429:            # was it a rate limit?
        wait = exc.response.headers.get("Retry-After", 60)  # read the header
        time.sleep(wait)                           # wait the right amount
```

Without this, tenacity retries immediately after a `429` and gets blocked again.

---

## Known limitation — retrying on all 4xx errors

`retry_if_exception_type(HTTPError)` retries on ALL HTTP errors including `401` and `404`. In production you should filter to only retry on `429` and `5xx`:

```python
def is_retryable(exc):
    if isinstance(exc, requests.exceptions.HTTPError):
        status = exc.response.status_code
        return status == 429 or status >= 500
    return isinstance(exc, requests.exceptions.ConnectionError)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(min=2, max=16),
    retry=retry_if_exception(is_retryable)
)
def get_with_retry(url, params):
    ...
```

---

## Key rules to remember

1. **429 and 5xx = retry, 4xx = stop** — never retry errors that are your fault
2. **Always read `Retry-After`** — the API tells you exactly how long to wait
3. **Use exponential backoff** — double the wait each attempt, don't hammer the server
4. **Separate retry logic from pagination logic** — one function, one job
5. **`before_sleep` hook** — use it to handle `429` waits specifically

---

## Quick comprehension check

- You hit a `429`. Your `Retry-After` header says `45`. What does your code do?
- You hit a `401`. Should tenacity retry? Why not?
- What does `wait_exponential(min=2, max=16)` mean in plain English?
- Why do you put retry logic in a separate function instead of inside the pagination loop?

---

*Next: Step 6 — Loading API data into a pipeline (flattening JSON, loading into pandas / PostgreSQL)*
