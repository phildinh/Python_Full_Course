# Error Handling — Study Notes

> **Purpose:** Quick recap of how to handle API errors gracefully in Python data pipelines.

---

## Why error handling matters

Without it, your pipeline crashes with a raw Python traceback when something goes wrong. In production — running on a schedule at 2am — you need it to catch the error, log what went wrong, and decide whether to retry or stop.

---

## The bad way — no error handling

```python
response = requests.get(url="https://api.example.com/data")
response.raise_for_status()
data = response.json()
```

If anything goes wrong here — network drops, API is down, bad key — your pipeline crashes with no context and nothing useful logged.

---

## The good way — try/except

```python
try:
    response = requests.get(
        url="https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": "Sydney",
            "units": "metric",
            "appid": API_KEY
        },
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code} — {e.response.text}")

except requests.exceptions.ConnectionError:
    print("Connection error — could not reach the API. Check your network.")

except requests.exceptions.Timeout:
    print("Timeout — the API took too long to respond.")

except requests.exceptions.RequestException as e:
    print(f"Unexpected error: {e}")
```

---

## The four exceptions you need to know

| Exception | When it fires | What it means |
|-----------|--------------|---------------|
| `HTTPError` | `raise_for_status()` on a `4xx` or `5xx` | Bad status code — API returned an error |
| `ConnectionError` | Can't reach the server at all | Network down, wrong URL, DNS failure |
| `Timeout` | Server took longer than `timeout` value | Server is slow or overloaded |
| `RequestException` | Anything else | Catch-all safety net |

> **Order matters.** Always put specific exceptions before the general `RequestException` catch-all. Python checks them top to bottom and stops at the first match.

---

## Which exception catches which error?

| Scenario | Exception caught |
|----------|-----------------|
| API returns `401`, `403`, `404`, `500` | `HTTPError` (via `raise_for_status()`) |
| Wrong URL, network is down | `ConnectionError` |
| Server too slow, `timeout=0.001` | `Timeout` |
| Anything else unexpected | `RequestException` |

---

## Retry vs stop — the most important decision

Not all errors are equal. The right response depends on *whose fault it is*.

| Code | Cause | Strategy | Why |
|------|-------|----------|-----|
| `4xx` | Your fault | **Stop** | Retrying won't fix a bad key or wrong URL |
| `5xx` | Their fault | **Retry** | Server errors are usually temporary |

**Key examples:**
- `401` — your API key is wrong or missing → **stop, fix the config**
- `404` — wrong endpoint URL → **stop, fix the code**
- `500` — server had a temporary problem → **retry, it may recover**
- `503` — server temporarily unavailable → **retry with a delay**

---

## How to tell which error you have inside the except block

```python
except requests.exceptions.HTTPError as e:
    status = e.response.status_code

    if status == 401:
        print("Auth failed — check your API key")
    elif status == 429:
        print("Rate limited — slow down")
    elif status >= 500:
        print("Server error — retry later")
```

---

## Testing your error handling — break things on purpose

| Test | How to trigger it | Expected output |
|------|------------------|-----------------|
| `HTTPError` | Change `"appid"` to `"key"` in params | `HTTP error: 401` |
| `ConnectionError` | Change URL to a fake domain | `Connection error` message |
| `Timeout` | Set `timeout=0.001` | `Timeout` message |

Always revert back to the working version after each test.

---

## Key rules to remember

1. **Always wrap API calls in try/except** — never let a raw traceback crash your pipeline
2. **Order exceptions from specific to general** — `HTTPError` before `RequestException`
3. **`4xx` = stop, `5xx` = retry** — the cause determines the strategy
4. **Always set `timeout=10`** — without it, a slow server hangs your pipeline indefinitely
5. **Log the status code and response text** — `e.response.status_code` and `e.response.text` give you the context you need to debug

---

## Quick comprehension check

- A `500` error fires. Which exception catches it? Should you retry or stop?
- A `401` error fires. Which exception catches it? Should you retry or stop?
- Why does the order of your `except` blocks matter?
- What happens if you don't set `timeout=10` and the API server hangs?

---

*Next: Step 4 — Pagination (looping through multiple pages of API results)*
