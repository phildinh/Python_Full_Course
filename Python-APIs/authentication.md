# Authentication — Study Notes

> **Purpose:** Quick recap of how to handle API authentication securely in Python data pipelines.

---

## Why authentication matters

Every real-world API you'll work with in a data pipeline requires you to prove who you are before handing over data. Get auth wrong and you get a `401` or `403` — and no data.

---

## The two most common auth patterns

| Pattern | How it works | Example APIs |
|---------|-------------|--------------|
| **API key in header** | Pass a secret key in the request header | Most data APIs |
| **Bearer token** | Pass a token in the `Authorization` header | OAuth APIs (Google, Salesforce) |

> As a junior DE, you will encounter API key auth most often.

---

## The wrong way — hardcoding your key

```python
# NEVER do this
response = requests.get(
    url="https://api.example.com/data",
    headers={"X-API-Key": "abc123secretkey"}   # exposed in your code
)
```

**Why this is dangerous:** If you push this to GitHub, your key is publicly exposed within seconds. Bots scan GitHub constantly for leaked keys.

---

## The right way — environment variables

The key lives in your environment, not your code.

### Setup (do this once per project)

**Step 1 — install python-dotenv:**

```bash
pip install python-dotenv
```

**Step 2 — create a `.env` file** in the same folder as your script:

```
OPENWEATHER_API_KEY=paste_your_key_here
```

**Step 3 — add `.env` to your `.gitignore`** so it never gets pushed to GitHub:

```
.env
```

**Step 4 — load it in your script:**

```python
import os
from dotenv import load_dotenv

load_dotenv()                              # reads .env into your environment
API_KEY = os.environ["MY_API_KEY"]        # retrieves the value
```

### Debugging tip — check your key is loading

If you suspect your `.env` isn't being read, run this first:

```python
from dotenv import load_dotenv
import os

load_dotenv()
print(os.environ.get("MY_API_KEY"))       # prints None if not found
```

If it prints `None`, your `.env` file is in the wrong folder or has a typo in the variable name.

---

## How to pass the key in the request

Always check the API documentation — different APIs expect the key in different places.

### Pattern A — key in headers (most common)

```python
response = requests.get(
    url="https://api.example.com/data",
    headers={"X-API-Key": API_KEY}
)
```

### Pattern B — Bearer token in Authorization header

```python
response = requests.get(
    url="https://api.example.com/data",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
```

### Pattern C — key as a query parameter (less common, less secure)

```python
response = requests.get(
    url="https://api.example.com/data",
    params={"appid": API_KEY}             # OpenWeatherMap uses this pattern
)
```

---

## The full working script (OpenWeatherMap example)

```python
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["OPENWEATHER_API_KEY"]

response = requests.get(
    url="https://api.openweathermap.org/data/2.5/weather",
    params={
        "q": "Sydney",
        "units": "metric",
        "appid": API_KEY
    }
)

response.raise_for_status()

data = response.json()

print(f"City:        {data['name']}")
print(f"Temperature: {data['main']['temp']}°C")
print(f"Description: {data['weather'][0]['description']}")
```

---

## Important — every API structures its response differently

Always inspect the raw JSON before extracting values:

```python
print(json.dumps(data, indent=2))
```

Notice in the OpenWeatherMap response:
- Temperature is nested under `data['main']['temp']`
- Weather description is inside a **list** — `data['weather'][0]['description']`
- The `[0]` is required to get the first item from the list

---

## Common auth errors

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorised` | Key not sent, sent incorrectly, or not yet activated | Check header/param name matches API docs. New keys can take up to 10 min to activate |
| `403 Forbidden` | Key is valid but doesn't have access to this resource | Check your plan tier or endpoint permissions |
| `None` printed from `os.environ.get()` | `.env` file not found or variable name typo | Check file location and spelling |

---

## Production note — what about cloud servers?

A `.env` file works locally but you can't put one on a production server. Real companies handle this with:

- **Cloud secret managers** — AWS Secrets Manager, Azure Key Vault, GCP Secret Manager
- **CI/CD environment variables** — set directly in GitHub Actions, Airflow, or your deployment platform

The pattern is the same — your code reads from `os.environ`, the secret just gets injected differently depending on the environment.

---

## Key rules to remember

1. **Never hardcode API keys** — always load from environment variables
2. **Always add `.env` to `.gitignore`** before your first commit
3. **Check the API docs** for where to pass the key — header, Bearer token, or query param
4. **New API keys can take time to activate** — a `401` on a fresh key doesn't always mean your code is wrong
5. **Always inspect raw JSON first** — every API structures its response differently

---

## Quick comprehension check

- Why should you never hardcode an API key in your script?
- Your `os.environ.get("MY_API_KEY")` prints `None`. What are the two most likely causes?
- What's the difference between Pattern A (key in header) and Pattern C (key as query param)?
- You deploy your pipeline to AWS. You can't use a `.env` file. What do you use instead?

---

*Next: Step 4 — Pagination (looping through multiple pages of API results)*
