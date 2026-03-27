# Static vs Dynamic Arrays — Time & Space Complexity
> Phil Dinh | Data Engineering Context

---

## The Big Picture — How It All Connects

```
Your Data
    ↓
How you STORE it → Static vs Dynamic Array
    ↓
How much MEMORY it uses → Space Complexity
    ↓
How fast you can ACCESS it → Time Complexity
    ↓
How you PROCESS it in a pipeline → Chunks vs Full Load
    ↓
Business outcome → Pipeline runs fast and cheap vs crashes
```

---

## 1. Memory — What Actually Happens

Your computer's RAM is like a street of houses. Each house has an address and holds one value.

```
Address:  100  101  102  103  104  105  106  107
Value:    [_]  [_]  [_]  [_]  [_]  [_]  [_]  [_]
```

**Critical rule: arrays need consecutive houses — no gaps.**

This is why reading by index is O(1) — the computer knows the start address, each house is the same size, so it calculates the exact address instantly. No searching needed.

---

## 2. Static Array — Fixed Block

You tell the computer upfront: *"Reserve me exactly N consecutive houses."*

```python
import numpy as np
arr = np.zeros(5)
# Computer reserves houses 100-104, locked forever
```

**What happens when full:**
```
Need a 6th slot?
❌ The next house (105) belongs to something else — you're stuck
```

**Complexity:**

| Operation | Complexity | Why |
|---|---|---|
| Read by index | O(1) | Direct address math |
| Write by index | O(1) | Direct address math |
| Memory used | O(n) | Exactly n houses, no waste |

**Trade-offs:**

| ✅ Pros | ❌ Cons |
|---|---|
| Fast access | Inflexible — fixed size |
| Memory efficient, no waste | Must know size upfront |
| Predictable performance | Crashes if data exceeds size |

---

## 3. Dynamic Array — The Doubling Trick

Starts small and grows automatically. Python's `list` is a dynamic array.

```python
arr = []
arr.append(10)   # fills slot 1
arr.append(20)   # fills slot 2
arr.append(30)   # fills slot 3 — now full
arr.append(40)   # no room — triggers resize
```

**What resize does step by step:**

```
Before:
Old block → Address 100-102: [10, 20, 30] ← full

Step 1: Find new block, double the size
New block → Address 200-205: [_, _, _, _, _, _]

Step 2: Copy everything across — O(n)
New block → Address 200-205: [10, 20, 30, _, _, _]

Step 3: Add new value
New block → Address 200-205: [10, 20, 30, 40, _, _]

Step 4: Release old block — free again
```

**Why double?** If it only added one slot, you'd resize on every append — O(n) copy every time. Doubling means resizes happen less and less frequently as the array grows.

**Complexity:**

| Operation | Complexity | Why |
|---|---|---|
| Append (normal) | O(1) average | Just fills an empty slot |
| Append (on resize) | O(n) | Must copy everything |
| Read by index | O(1) | Still direct address math |
| Memory used | O(n) to O(2n) | Always keeps extra empty slots |

**Trade-offs:**

| ✅ Pros | ❌ Cons |
|---|---|
| Flexible — grows automatically | Copying is expensive on resize |
| No upfront size needed | Wastes some memory (empty slots) |
| Never crashes on unexpected volume | Memory usage less predictable |

---

## 4. Space Complexity

Answers: *"As my data grows, how does my memory usage grow?"*

Same Big O notation as time complexity — but measuring memory instead of steps.

| Space Complexity | Meaning | Example |
|---|---|---|
| O(1) | Fixed memory no matter what | A single counter variable |
| O(n) | Memory grows with data | Storing every row in a list |
| O(n²) | Memory explodes | Storing every pair combination |

**Code examples:**

```python
# O(1) space — only one variable regardless of data size
total = 0
for row in huge_dataset:
    total += row["revenue"]   # one variable, always

# O(n) space — grows with every row
all_rows = []
for row in huge_dataset:
    all_rows.append(row)   # one slot per row

# O(n²) space — dangerous at scale
pairs = []
for row1 in dataset:
    for row2 in dataset:
        pairs.append((row1, row2))   # explodes fast
```

---

## 5. Time vs Space Trade-off

**You almost always trade one for the other:**
- More memory = faster processing
- Less memory = slower processing

| Approach | Time | Space | When To Use |
|---|---|---|---|
| Load everything into memory | Fast O(1) access | O(n) — expensive | Small datasets, dashboards |
| Process row by row | Slower, more passes | O(1) — cheap | Huge datasets, limited RAM |
| Build a lookup dict | O(1) lookup | O(n) extra memory | Speed matters more than memory |
| Nested loop | O(n²) time | O(1) space | Almost never |

---

## 6. Real Pipeline Examples — Easy To Reality

### Level 1 — Small Data, Speed Matters
*Power BI dashboard, 50,000 rows, refreshes hourly*

```python
# Load everything — O(n) space, O(1) access after load
df = pd.read_csv("sales.csv")

# Pre-compute all summaries once
monthly_totals = df.groupby("month")["revenue"].sum()
top_products = df.groupby("product")["revenue"].sum().nlargest(10)
```

Trade-off: use more memory upfront → dashboard queries are instant.

---

### Level 2 — Large Data, Memory Limited
*ETL pipeline, 50 million rows, limited server RAM*

```python
# O(1) space — never load more than 50,000 rows at once
running_total = 0
product_totals = {}

for chunk in pd.read_csv("transactions.csv", chunksize=50000):
    running_total += chunk["revenue"].sum()

    for product, revenue in chunk.groupby("product")["revenue"].sum().items():
        product_totals[product] = product_totals.get(product, 0) + revenue
```

Trade-off: minimal memory → takes slightly longer but never crashes.

---

### Level 3 — FMCG / Retail Pipeline
*Weekly inventory data — unknown number of SKUs*

```python
# Bad — static thinking, fixed size assumption
inventory = np.zeros(10000)   # assumes max 10,000 SKUs
# One week you get 10,500 SKUs — pipeline crashes

# Good — dynamic thinking, grows with data
inventory = {}
for row in inventory_file:
    inventory[row["sku_id"]] = row["stock_level"]
# Handles any number of SKUs automatically
```

---

### Level 4 — Spark At Scale
*Broadcast join = static thinking. Regular join = dynamic thinking.*

```python
# Broadcast join — send small lookup table to every machine once
# Static array thinking — O(1) lookup per row
from pyspark.sql.functions import broadcast
result = orders.join(broadcast(products), "product_id")

# Regular join — Spark shuffles large data across machines
# Dynamic thinking — handles unknown sizes
result = orders.join(products, "product_id")
```

---

## 7. The Decision Framework

```
DATA SIZE KNOWN + SMALL?
    → Static array / full load into memory
    → O(n) space, O(1) access
    → Use for: dashboards, lookups, reference tables

DATA SIZE UNKNOWN + LARGE?
    → Dynamic array / chunk processing
    → O(1) space, slightly more passes
    → Use for: ETL pipelines, large CSV processing

NEED FAST LOOKUPS ON LARGE DATA?
    → Dict (hash map) — static size output, dynamic build
    → O(n) space for the dict, O(1) per lookup
    → Use for: enrichment, joins, deduplication

PROCESSING A STREAM?
    → Always dynamic — can't know size upfront
    → O(1) space with running aggregations
    → Use for: Kafka, real-time pipelines, event processing
```

---

## 8. Quick Reference — Static vs Dynamic

| | Static Array | Dynamic Array |
|---|---|---|
| Size | Fixed upfront | Grows automatically |
| Memory | Exactly n — no waste | n to 2n — some buffer |
| Read speed | O(1) | O(1) |
| Append | Not possible | O(1) average |
| Resize cost | N/A | O(n) when triggered |
| Python example | `numpy array` | `list` |
| DE use case | Fixed schema, known size | Unknown volume, streaming |

---

## 9. The One Rule

> **Memory and speed pull in opposite directions. A senior DE knows which one to sacrifice based on data size, infrastructure cost, and business deadline.**

- Junior DE: loads everything into memory because it's easy
- Senior DE: asks *"how big will this get in 6 months?"* before writing a single line

---

## 10. How This Connects To Your Existing Knowledge

| Concept From Previous Sessions | Connection Here |
|---|---|
| Dict lookup O(1) | Trading O(n) space for O(1) time |
| Nested loop O(n²) | Worst case for both time AND space |
| Sliding window | O(1) space — only track the window, not all data |
| Prefix sums | O(n) space trade-off for O(1) query time |
| Chunk processing | Dynamic array thinking in practice |

---

*Next session: Linked Lists*
