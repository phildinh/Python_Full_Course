# Pagination — Study Notes

> **Purpose:** Quick recap of how to loop through paginated API responses in Python data pipelines.

---

## Why pagination matters

APIs never return all records in one call — that would be too slow and expensive for both sides. Instead they return data in chunks (pages) and expect you to loop through them.

If you don't handle pagination, your pipeline silently loads only the first page and you never know you're missing data. That's a serious data quality problem — no error, no warning, just incomplete data.

---

## The two most common pagination patterns

| Pattern | Parameters | Exit condition | Example API |
|---------|-----------|----------------|-------------|
| **Offset-based** | `_start`, `_limit` | Empty response | JSONPlaceholder |
| **Page-based** | `page=1`, `page=2` | `next` is null | Rick and Morty API |

> Always inspect the raw JSON response first with `json.dumps(data, indent=2)` before writing the loop — every API structures its pagination metadata differently.

---

## Pattern 1 — Offset-based pagination

Used when the API takes a starting position and a limit.

```
_start=0,  _limit=10  → records 1–10
_start=10, _limit=10  → records 11–20
_start=20, _limit=10  → records 21–30
```

**Exit condition:** empty response means no more records.

```python
import requests

all_todos = []
start = 0
limit = 10

while True:
    response = requests.get(
        url="https://jsonplaceholder.typicode.com/todos",
        params={
            "_limit": limit,
            "_start": start
        }
    )
    response.raise_for_status()

    batch = response.json()

    if not batch:           # empty response = no more records
        break

    all_todos.extend(batch)
    print(f"Fetched records {start + 1} to {start + len(batch)}")
    start += limit          # move the window forward

print(f"Total todos fetched: {len(all_todos)}")
```

---

## Pattern 2 — Page-based pagination

Used when the API returns a `next` URL or page metadata in the response.

**What the `info` section looks like:**

```json
"info": {
  "count": 826,
  "pages": 42,
  "next": "https://rickandmortyapi.com/api/character?page=2",
  "prev": null
}
```

**How `next` and `prev` behave:**

```
page 1:  prev = null,           next = "...?page=2"
page 2:  prev = "...?page=1",   next = "...?page=3"
...
page 42: prev = "...?page=41",  next = null   ← stop here
```

**Exit condition:** when `next` is null, you're on the last page.

```python
import requests

all_characters = []
page = 1

while True:
    try:
        response = requests.get(
            url="https://rickandmortyapi.com/api/character",
            params={"page": page}
        )
        response.raise_for_status()
        data = response.json()

        all_characters.extend(data["results"])
        print(f"Fetched page {page} — {len(data['results'])} characters")

        if not data["info"]["next"]:   # null next = last page
            break

        page += 1

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code} — {e.response.text}")
        break

    except requests.exceptions.ConnectionError:
        print("Connection error — could not reach the API.")
        break

    except requests.exceptions.Timeout:
        print("Timeout — the API took too long to respond.")
        break

    except requests.exceptions.RequestException as e:
        print(f"Unexpected error: {e}")
        break

print(f"Total characters fetched: {len(all_characters)}")
```

---

## `extend` vs `append` — critical difference

Always use `extend` when combining pages — never `append`.

```python
all_records = []

# append adds the whole page as one item — WRONG
all_records.append([record1, record2, record3])
# result: [[record1, record2, record3]]   ← list of lists

# extend adds each item individually — CORRECT
all_records.extend([record1, record2, record3])
# result: [record1, record2, record3]     ← flat list
```

---

## Always put pagination inside try/except

The `try` block must contain everything — the request, the parse, the extend, and the exit check. The `except` blocks come immediately after `try` closes. Break on errors to stop the loop cleanly.

```python
while True:
    try:
        # request
        # raise_for_status
        # parse
        # extend
        # check exit condition
        # increment page
    except ...:
        break
```

---

## What to look for in the response before writing the loop

| What you see | Pagination type | Exit condition |
|-------------|-----------------|----------------|
| `_start`, `_limit` params | Offset-based | Empty response |
| `page` param + `next` field | Page-based | `next` is null |
| `page` param + `total_pages` field | Page-based | `page > total_pages` |
| `cursor` or `after` field | Cursor-based | `next_cursor` is null |

---

## Production note — what happens when an error occurs mid-pagination?

Simply breaking on error loses all progress. In production you want **retry logic with exponential backoff**:

```
attempt 1 fails → wait 2 seconds → retry
attempt 2 fails → wait 4 seconds → retry
attempt 3 fails → wait 8 seconds → retry
then log and stop
```

This is covered in Step 5 — Rate limiting and retries.

---

## Key rules to remember

1. **Always inspect raw JSON first** — understand the pagination structure before writing the loop
2. **Use `extend` not `append`** — you want a flat list of records, not a list of pages
3. **Check the right exit condition** — empty response for offset, `next=null` for page-based
4. **Always wrap in try/except** — errors mid-loop should break cleanly, not crash
5. **Never assume one page is enough** — always paginate, even if you think the dataset is small

---

## Quick comprehension check

- You get back a response with `"next": null`. What do you do?
- You're on page 15 of 42 and get a `500` error. Your code breaks. What's the smarter production behaviour?
- What's the difference between `extend` and `append` when building your records list?
- You inspect a new API's response and see `"total_count": 500` and `"per_page": 50`. How many pages do you expect to loop through?

---

*Next: Step 5 — Rate limiting and retries (exponential backoff, the `tenacity` library)*
