# The `requests` Library — Study Notes

> **Purpose:** Quick recap of how to use Python's `requests` library to call an API and parse the response.

---

## Why `requests`?

Python has a built-in way to make HTTP calls (`urllib`) but it's verbose and painful. The `requests` library wraps all that complexity into clean, readable code. It's the industry standard — every data engineer uses it.

```bash
pip install requests
```

---

## The core pattern

Every API call in Python follows the same four steps:

```
1. Make the call       →  requests.get()
2. Check it worked     →  response.raise_for_status()
3. Parse the data      →  response.json()
4. Extract the values  →  data["key"]["nested_key"]
```

---

## Step 1 — Make the call

```python
import requests

response = requests.get(
    url="https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": "-33.87",
        "longitude": "151.21",
        "current_weather": "true"
    }
)
```

**Key points:**
- Pass parameters as a dictionary with `params={}` — `requests` builds the query string for you
- So `{"latitude": "-33.87", "longitude": "151.21"}` becomes `?latitude=-33.87&longitude=151.21` in the URL
- Always use `timeout=10` in production so a slow server doesn't hang your pipeline

---

## Step 2 — Check it worked

```python
response.raise_for_status()
```

**Why this matters:** Without it, a `400` or `500` response silently continues and tries to parse bad data — causing confusing errors downstream. `raise_for_status()` throws a loud, readable error immediately if the status code is anything other than `2xx`.

**Also useful:**

```python
print(response.status_code)   # 200 = success
```

---

## Step 3 — Parse the data

```python
data = response.json()
```

This converts the raw JSON string in the response body into a Python dictionary you can navigate.

**To pretty-print for debugging:**

```python
import json
print(json.dumps(data, indent=2))
```

---

## Step 4 — Extract the values

The response is a nested dictionary. Navigate it with key access:

```python
# Top-level key
timezone  = data["timezone"]         # "GMT"
elevation = data["elevation"]        # 69.0

# Nested key (one level deeper)
temp      = data["current_weather"]["temperature"]    # 27.1
windspeed = data["current_weather"]["windspeed"]      # 10.5
winddir   = data["current_weather"]["winddirection"]  # 84
is_day    = data["current_weather"]["is_day"]         # 1
```

**Mental model — picture the structure as a tree:**

```
data
├── timezone              →  "GMT"
├── elevation             →  69.0
└── current_weather       ←  nested dict
    ├── temperature       →  27.1
    ├── windspeed         →  10.5
    ├── winddirection     →  84
    └── is_day            →  1
```

---

## The full working script

```python
import requests
import json

response = requests.get(
    url="https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": "-33.87",
        "longitude": "151.21",
        "current_weather": "true"
    }
)

response.raise_for_status()

data = response.json()

temp      = data["current_weather"]["temperature"]
windspeed = data["current_weather"]["windspeed"]
winddir   = data["current_weather"]["winddirection"]
is_day    = data["current_weather"]["is_day"]
timezone  = data["timezone"]
elevation = data["elevation"]

print(f"Temperature:   {temp}°C")
print(f"Wind speed:    {windspeed} km/h")
print(f"Wind direction:{winddir}°")
print(f"Daytime:       {'Yes' if is_day == 1 else 'No'}")
print(f"Timezone:      {timezone}")
print(f"Elevation:     {elevation}m")
```

---

## Common errors and what they mean

| Error | Cause | Fix |
|-------|-------|-----|
| `400 Bad Request` | Wrong or missing parameters | Check your `params` dictionary keys and values |
| `401 Unauthorised` | Auth not sent correctly | Check your API key header format |
| `404 Not Found` | Wrong endpoint URL | Check the URL for typos |
| `429 Too Many Requests` | Rate limited | Wait, then retry |
| `500 Server Error` | API side problem | Log it, retry later |

---

## Key rules to remember

1. **Always call `raise_for_status()`** — never silently continue on a bad response
2. **Pass params as a dict** — let `requests` build the query string, don't manually concatenate URLs
3. **Use `json.dumps(data, indent=2)`** to debug and understand the response structure before extracting values
4. **Navigate nested dicts with chained keys** — `data["current_weather"]["temperature"]`
5. **Always set `timeout=10`** in production pipelines

---

## Quick comprehension check

- What does `raise_for_status()` do and why do you always include it?
- You get back a `400`. Where do you look first?
- What's the difference between `response.json()` and `json.dumps(data, indent=2)`?
- How do you extract a value that is two levels deep in the response dictionary?

---

*Next: Step 3 — Authentication (API keys, Bearer tokens, environment variables)*
