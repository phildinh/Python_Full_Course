# HTTP Basics — Study Notes

> **Purpose:** Quick recap of HTTP fundamentals before writing API code in Python.

---

## What is HTTP?

HTTP is the language your Python script uses to talk to an API — the same language your browser uses when you visit a website.

**The analogy:** Think of it like sending a letter through the post.
- You write a letter → **the request**
- You address it to a location → **the URL**
- You say what you want → **the method**
- They write back → **the response**
- They tell you if it worked → **the status code**

---

## The HTTP Request — what YOU send

Every request has four parts:

### 1. The URL (where you're sending it)

```
https://api.openweathermap.org/data/2.5/weather?q=Sydney&units=metric
```

| Part | Example | What it is |
|------|---------|------------|
| Protocol | `https://` | Secure HTTP |
| Domain | `api.openweathermap.org` | Who you're talking to |
| Endpoint | `/data/2.5/weather` | Which resource you want |
| Query params | `?q=Sydney&units=metric` | Your filters and options |

### 2. The Method (what you want to do)

| Method | Meaning | When you use it |
|--------|---------|-----------------|
| `GET` | "Give me data" | Pulling records, reports, exports |
| `POST` | "Here's data, do something with it" | Sending a payload, triggering a job |

> As a data engineer, you will use `GET` 90% of the time.

### 3. The Headers (metadata you send)

Key-value pairs that travel alongside your request.

| Header | Example value | What it does |
|--------|--------------|--------------|
| `Authorization` | `Bearer abc123` | Proves who you are |
| `Content-Type` | `application/json` | Format of data you're sending |
| `Accept` | `application/json` | Format you want back |

### 4. The Body (POST requests only)

When you're pushing data to the API, the payload goes here — usually as JSON. Not used in `GET` requests.

---

## The HTTP Response — what the SERVER sends back

Every response has four parts:

### 1. The Status Code (did it work?)

| Code | Meaning | What to do |
|------|---------|------------|
| `200` | Success | Parse the response |
| `201` | Created (POST worked) | Parse the response |
| `400` | Bad request — your fault | Check your parameters |
| `401` | Unauthorised | Check how you're sending your API key |
| `403` | Forbidden | You don't have access to this resource |
| `404` | Not found | Check the endpoint URL |
| `429` | Rate limited | Wait, then retry |
| `500` | Server error — their fault | Log it, retry later |
| `503` | Service unavailable | Same as 500 |

> **Always check the status code first.** Never assume a 200. In Python, always call `response.raise_for_status()`.

### 2. The Response Headers (metadata from the server)

| Header | What it tells you |
|--------|-------------------|
| `Content-Type: application/json` | Body is JSON — safe to parse |
| `Retry-After: 30` | Wait 30 seconds after a 429 |
| `X-RateLimit-Remaining: 45` | How many calls you have left |

### 3. The Response Body (the actual data)

Almost always JSON in modern APIs. This is what you parse into a Python dictionary.

### 4. Protocol version

Usually `HTTP/1.1` or `HTTP/2`. You rarely need to think about this.

---

## Request vs Response — side by side

| Direction | Part | Contains |
|-----------|------|----------|
| You → Server | Request headers | Your auth, content preferences |
| You → Server | Request body | Data you're sending (POST only) |
| Server → You | Response headers | Status metadata, rate limit info |
| Server → You | Response body | The JSON data you wanted |

---

## Key rules to remember

1. **Status code first, body second** — always check if the call succeeded before parsing data.
2. **401 ≠ broken key** — it means your key wasn't sent correctly. Check the header format first.
3. **429 = slow down** — read the `Retry-After` header and wait before retrying.
4. **Never hardcode your API key** — load it from an environment variable: `os.environ["MY_API_KEY"]`.
5. **Always set `timeout`** — without it, a slow server can hang your pipeline indefinitely.

---

## Quick comprehension check

Before moving to Step 2 (the `requests` library), make sure you can answer:

- You get a `401`. What's the first thing you check?
- You get a `429`. What do you do?
- What's the difference between a request header and a request body?
- You want to fetch sales records from a CRM API. Which method do you use?

---

*Next: Step 2 — The `requests` library (writing real code against a live API)*
