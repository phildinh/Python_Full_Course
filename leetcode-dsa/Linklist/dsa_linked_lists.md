# Linked Lists — Recap Notes
> Phil Dinh | Data Engineering Context

---

## 1. Why Linked Lists Exist — The Problem With Arrays

Inserting in the middle of an array is O(n) — everything shifts right to make room.

```python
nums = [10, 20, 30, 40, 50]
nums.insert(2, 99)   # shifts 30, 40, 50 one step right — expensive
```

At 10 million rows, that shifting costs real time and money.

**Linked lists solve this — insertion and deletion are O(1).**

---

## 2. The Core Idea — Treasure Hunt

Each node holds two things:
- Its **value** — the data
- A **pointer** — the address of the next node

```
head
  ↓
[10 | →] → [20 | →] → [30 | →] → [40 | None]
```

- **head** = entry point into the list
- **None** = end of the list
- You can only move forward — follow the chain from head

---

## 3. Why You Can't Read By Index — O(n)

Arrays sit in consecutive memory — the computer calculates any address instantly. O(1).

Linked list nodes are scattered anywhere in memory. The only way to find node 4 is to walk the chain from head, following pointers one by one.

> Start at head → follow next → follow next → follow next → arrive at node 4

That's O(n) — you visit every node before the one you want.

---

## 4. The Code — Full Implementation

```python
class Node:
    def __init__(self, value):
        self.value = value   # the data
        self.next = None     # pointer to next node

class LinkedList:
    def __init__(self):
        self.head = None     # empty list — no starting point yet

    # Traverse — visit every node
    def traverse(self):
        current = self.head
        while current is not None:
            print(current.value)
            current = current.next   # follow the pointer forward

    # Insert at the beginning — O(1)
    def insert_at_head(self, value):
        new_node = Node(value)
        new_node.next = self.head    # point new node to current head
        self.head = new_node         # new node becomes the head

    # Insert at the end — O(n)
    def insert_at_tail(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:   # walk to the last node
            current = current.next
        current.next = new_node           # point last node to new node

    # Insert after a specific value — O(n) to find, O(1) to insert
    def insert_after(self, target, value):
        current = self.head
        while current is not None:
            if current.value == target:
                new_node = Node(value)
                new_node.next = current.next  # step 1 — point new node forward
                current.next = new_node       # step 2 — point target to new node
                return
            current = current.next
        print(f"{target} not found")

    # Delete a node — O(n) to find, O(1) to delete
    def delete(self, value):
        if self.head is None:
            print("List is empty")
            return
        if self.head.value == value:
            self.head = self.head.next   # second node becomes new head
            return
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next  # skip over the deleted node
                return
            current = current.next
        print(f"{value} not found")
```

---

## 5. Operation Walkthrough

### Traversal
```
head → [10] → [20] → [30] → None

current = head (10)  → print 10  → move to next
current = node (20)  → print 20  → move to next
current = node (30)  → print 30  → move to next
current = None       → stop
```

### Insert After — Critical Order

```
Before: [10] → [20] → [30]
Insert 15 after 10:

Step 1: new_node.next = current.next  →  [15] points to [20]
Step 2: current.next = new_node       →  [10] points to [15]

After:  [10] → [15] → [20] → [30]
```

⚠️ Order matters — do step 1 before step 2. If you reverse them, you lose the pointer to [20] forever.

### Delete — Skip Over The Node

```
Before: [10] → [20] → [30] → [40]
Delete 20:

current.next = current.next.next
= node10.next = node30

After:  [10] → [30] → [40]
node20 is skipped and forgotten
```

---

## 6. Complexity Summary

| Operation | Time | Why |
|---|---|---|
| Traverse | O(n) | Visit every node |
| Read by index | O(n) | Must walk from head |
| Insert at head | O(1) | Just update two pointers |
| Insert at tail | O(n) | Must walk to the end first |
| Insert in middle | O(1) | Just update two pointers once found |
| Delete head | O(1) | Just update head pointer |
| Delete middle/tail | O(n) | Must walk to find the node |

---

## 7. Arrays vs Linked Lists

| | Array | Linked List |
|---|---|---|
| Memory layout | Consecutive — predictable | Scattered — flexible |
| Read by index | O(1) — direct math | O(n) — walk the chain |
| Insert at middle | O(n) — shift everything | O(1) — update pointers |
| Delete at middle | O(n) — shift everything | O(1) — skip the node |
| Size | Fixed or costly resize | Grows freely, no copying |
| Best for | Fast reads, known size | Fast inserts/deletes, unknown size |

---

## 8. Where Linked Lists Live In DE Work

You don't build linked lists from scratch in production. But they explain why your tools behave the way they do.

| Real Tool | Node Value | Next Pointer | Why It's A Linked List |
|---|---|---|---|
| Airflow DAG | Task logic | Next task | Tasks chain in order, each only knows what's next |
| Git commits | Code changes | Parent commit | `git log` traverses the chain from HEAD |
| Kafka partition | Message payload | Next offset | Consumers follow offsets forward |
| ETL pipeline | Transformation step | Next step | Each step hands off to the next |

---

## 9. The Three Rules To Remember

**Insertion:**
> Always point the new node forward first, then update the previous node. Reverse the order and you lose the chain.

**Deletion:**
> You don't remove the node — you make everyone skip over it. `current.next = current.next.next`

**Traversal:**
> Always start at head. Always stop at None. Use `current = current.next` to move forward.

---

## 10. How This Connects To Everything Else

| Concept | Connection To Linked Lists |
|---|---|
| O(n) traversal | Same as scanning an array — visit everything once |
| O(1) insertion | Better than arrays for middle inserts — no shifting |
| Pointer thinking | Foundation for trees, graphs, and queues coming next |
| Dynamic arrays | Both grow flexibly — linked lists just don't need to copy |

---

*Next session: Hash Maps / Hash Tables*
