# DSA Arrays — Recap Notes
> Phil Dinh | Started March 2026

---

## 1. Big O Notation

**What it is:** How many steps your code takes as your data grows. Not seconds — steps.

**n = size of your data**

| Big O | Name | Mental Model | Example |
|---|---|---|---|
| O(1) | Constant | Always one step, no matter what | Dict lookup by key |
| O(n) | Linear | Visit every item once | Loop through a list |
| O(n log n) | Log linear | Sort then scan | Python's `.sort()` |
| O(n²) | Quadratic | Every item checks every item | Nested loop |

**At scale — why it matters:**

| n (rows) | O(n) | O(n²) |
|---|---|---|
| 1,000 | 1,000 | 1,000,000 |
| 500,000 | 500,000 | 250,000,000,000 |
| 1,000,000 | 1,000,000 | 1,000,000,000,000 |

> The difference between O(n) and O(n²) at 1M rows = pipeline finishes in seconds vs runs for days.

---

## 2. Arrays — The Basics

An array is a row of lockers. Each locker has an index (starting at 0) and holds one value. All lockers sit next to each other in memory.

```python
nums = [10, 20, 30, 40, 50]
#        0    1    2    3    4   ← index
```

**Core operations:**

| Operation | Example | Complexity | Why |
|---|---|---|---|
| Read by index | `nums[2]` | O(1) | Direct math, no searching |
| Search for value | `if 30 in nums` | O(n) | Must check each one |
| Append to end | `nums.append(60)` | O(1) | Just add to the end |
| Insert at middle | `nums.insert(2, 99)` | O(n) | Must shift everything right |

---

## 3. Dict Lookup Optimisation

**The pattern:** Large dataset + small reference dataset = build a dict from the small one, loop the large one once.

**Bad way — O(n²):**
```python
# For every order, scan every product
for order in orders:
    for product in products:
        if order["product_id"] == product["product_id"]:
            # match found
```

**Good way — O(n):**
```python
# Step 1 — build lookup dict once — O(m)
product_lookup = {p["product_id"]: p["name"] for p in products}

# Step 2 — single pass, instant lookup — O(n)
for order in orders:
    product_name = product_lookup.get(order["product_id"])  # O(1)
```

**Use `.get()` not direct lookup** — protects against missing keys in messy data.

**Real DE uses:**
- Enriching datasets (orders + products)
- Mapping IDs to names
- Joining small reference tables to large fact tables
- Same concept as a database index under the hood

---

## 4. Two Pointer

**What it is:** Two variables pointing to positions in a sorted array, moving intelligently so you never check the same pair twice.

**Requires sorted data.** If unsorted — sort first, then apply. Total cost = O(n log n).

### Pattern A — Squeeze Inward (sum target)

Pointers start at opposite ends and move toward each other.

```python
nums = [-10, -3, 0, 5, 12, 18, 24]
target = 14

left = 0
right = len(nums) - 1

while left < right:
    total = nums[left] + nums[right]
    if total == target:
        print(nums[left], nums[right])
        break
    elif total < target:
        left += 1       # need bigger number
    else:
        right -= 1      # need smaller number
```

### Pattern B — Move Forward Together (gap target)

Both pointers start at the left and move forward together.

```python
deliveries = [10, 25, 40, 70, 85, 100, 130]
target_gap = 60

left = 0
right = 1

while right < len(deliveries):
    gap = deliveries[right] - deliveries[left]
    if gap == target_gap:
        print(deliveries[left], deliveries[right])
        left += 1
        right += 1
    elif gap < target_gap:
        right += 1      # gap too small, widen it
    else:
        left += 1       # gap too big, shrink it
```

**Two pointer patterns:**

| Pattern | Pointers | Used When |
|---|---|---|
| Squeeze inward | → ← | Finding pairs that sum to a target |
| Move forward together | → → | Finding pairs with a target gap |

**Real DE uses:**
- Finding overlapping date ranges
- Detecting duplicate transactions on sorted IDs
- Merging two sorted datasets
- SQL `LAG()` / `LEAD()` window functions under the hood

---

## 5. Sliding Window

**What it is:** A window of fixed size k slides across the array one step at a time. Instead of recalculating the whole sum, you subtract what leaves and add what enters.

**Does NOT require sorted data** — order matters because you're looking for consecutive sequences.

```
new sum = old sum - value leaving left + value entering right
```

```python
sales = [100, 200, 300, 400, 500, 600, 700]
k = 3   # window size

# Step 1 — calculate first window
window_sum = sum(sales[0:k])
best_sum = window_sum
best_start = 0

# Step 2 — slide forward
for i in range(1, len(sales) - k + 1):
    window_sum = window_sum - sales[i - 1] + sales[i + k - 1]
    #                         ↑ leaves left   ↑ enters right
    if window_sum > best_sum:
        best_sum = window_sum
        best_start = i

print(f"Best {k} days: {sales[best_start: best_start + k]}")
print(f"Total: {best_sum}")
```

**Real DE uses:**
- 7-day rolling average sales → `df.rolling(7).mean()` in pandas
- Peak hour detection in transactions
- Fraud detection — unusual spend in any 5 minute window
- Consecutive days below reorder threshold

---

## 6. Prefix Sums

> 🔄 Coming back to this tomorrow

**The idea:** Build a running total array once — O(n). Then answer any range sum query instantly — O(1).

```
sales  = [100, 200, 300, 400, 500, 600, 700]
prefix = [0,   100, 300, 600, 1000,1500,2100,2800]

# Any range sum = prefix[right + 1] - prefix[left]
```

**Real DE uses:**
- Running total revenue by day
- Cumulative inventory consumed
- Dashboard range queries
- SQL `SUM() OVER(ORDER BY date)` under the hood

---

## 7. Key Rules To Remember

| Rule | Detail |
|---|---|
| Nested loop = danger | Always ask — can I use a dict instead? |
| Two pointer needs sorted data | Sort first if unsorted — O(n log n) total |
| Sliding window needs original order | Never sort before sliding window |
| `.get()` over direct dict lookup | Protects against missing keys in real data |
| `while left < right` not `while True` | Prevents infinite loop when no answer exists |

---

## 8. How DSA Maps To Real DE Tools

| What You Learned | Real DE Tool | Example |
|---|---|---|
| Single pass O(n) | pandas vectorisation | `df["col"].apply(func)` |
| Dict lookup O(1) | pandas merge / SQL JOIN | `df.merge(lookup_df, on="id")` |
| Two pointer | SQL window functions | `LAG()`, `LEAD()` |
| Sliding window | pandas rolling | `df.rolling(7).mean()` |
| Prefix sums | SQL cumulative sum | `SUM() OVER(ORDER BY date)` |

---

*Next session: Prefix sums + start of next data structure topic*
