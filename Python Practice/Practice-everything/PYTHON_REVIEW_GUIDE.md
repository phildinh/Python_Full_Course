# Python Review Guide - Complete Warm-Up

This is a systematic walkthrough of everything you need to remember. Read each section, run the code examples locally, and make sure you can explain WHY each part works.

---

## 1. DATA STRUCTURES FUNDAMENTALS

### Lists
```python
# Create
my_list = [1, 2, 3, 4, 5]

# Access
first = my_list[0]        # 1
last = my_list[-1]        # 5

# Slice
subset = my_list[1:3]     # [2, 3] (start at 1, stop before 3)
every_other = my_list[::2] # [1, 3, 5] (start, stop, step)

# Modify
my_list.append(6)         # Add to end: [1, 2, 3, 4, 5, 6]
my_list.insert(0, 0)      # Insert at position: [0, 1, 2, 3, 4, 5, 6]
my_list.remove(3)         # Remove value: [0, 1, 2, 4, 5, 6]
popped = my_list.pop()    # Remove & return last: popped=6

# Check membership
3 in my_list              # False
2 in my_list              # True

# Length
len(my_list)              # 6
```

**WHY**: Lists are ordered, mutable (changeable), and the most common container in Python.

---

### Dictionaries
```python
# Create
person = {
    'name': 'Phil',
    'age': 28,
    'city': 'Sydney'
}

# Access
name = person['name']           # 'Phil'
age = person.get('age')         # 28
unknown = person.get('email', 'N/A')  # 'N/A' (default if key missing)

# Add/Update
person['email'] = 'phil@example.com'
person['age'] = 29

# Delete
del person['email']

# Iterate
for key in person:
    print(key, person[key])

for key, value in person.items():
    print(f"{key}: {value}")

# Check membership
'name' in person           # True
'email' in person          # False

# Get all keys/values
keys = person.keys()       # dict_keys(['name', 'age', 'city'])
values = person.values()   # dict_values(['Phil', 29, 'Sydney'])
```

**WHY**: Dicts are key-value stores. Fast lookup (O(1)). Essential for data pipelines.

---

### Sets
```python
# Create (unordered, unique values only)
colors = {'red', 'green', 'blue'}
numbers = set([1, 2, 2, 3, 3, 3])  # {1, 2, 3}

# Add/Remove
colors.add('yellow')
colors.remove('red')        # Error if not found
colors.discard('purple')    # No error if not found

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}

union = a | b              # {1, 2, 3, 4}
intersection = a & b       # {2, 3}
difference = a - b         # {1}

# Check membership
2 in a                      # True
```

**WHY**: Sets remove duplicates and enable fast membership checks (O(1)). Use when you need unique values.

---

## 2. LOOPS & ITERATION

### For Loop
```python
# Basic iteration
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Loop through list with index
fruits = ['apple', 'banana', 'cherry']
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")  # 0: apple, 1: banana, etc

# Loop through dict
person = {'name': 'Phil', 'age': 28}
for key, value in person.items():
    print(f"{key}: {value}")

# Loop through multiple lists together
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

### While Loop
```python
count = 0
while count < 5:
    print(count)
    count += 1

# Break & Continue
while True:
    user_input = input("Enter 'quit' to stop: ")
    if user_input == 'quit':
        break  # Exit loop
    if user_input == 'skip':
        continue  # Skip to next iteration
    print(f"You entered: {user_input}")
```

**WHY**: For loops are for known iterations. While loops are for conditional stopping.

---

## 3. LIST COMPREHENSION (CRITICAL FOR DATA WORK)

```python
# Basic: transform a list
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]  # [1, 4, 9, 16, 25]

# With condition: filter
evens = [x for x in numbers if x % 2 == 0]  # [2, 4]

# Combined: transform + filter
squared_evens = [x**2 for x in numbers if x % 2 == 0]  # [4, 16]

# Dict comprehension
my_dict = {x: x**2 for x in numbers}  # {1: 1, 2: 4, 3: 9, ...}

# Set comprehension
unique_lengths = {len(word) for word in ['apple', 'app', 'application']}  # {3, 5, 11}
```

**WHY**: Comprehensions are faster, more readable, and more "Pythonic" than loops. Use them everywhere.

---

## 4. FUNCTIONS

### Basic Structure
```python
def greet(name, greeting="Hello"):
    """This is a docstring - describes what the function does."""
    return f"{greeting}, {name}!"

# Call it
result = greet("Phil")              # "Hello, Phil!"
result = greet("Phil", "Hi")        # "Hi, Phil!"
result = greet(name="Phil", greeting="Hey")  # Keyword args
```

### Args & Kwargs
```python
# *args: accept any number of positional arguments
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

sum_all(1, 2, 3, 4, 5)  # 15

# **kwargs: accept any number of keyword arguments
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Phil", age=28, city="Sydney")
# name: Phil
# age: 28
# city: Sydney
```

### Lambda (Anonymous Functions)
```python
# Short function in one line
square = lambda x: x**2
square(5)  # 25

# Often used with map/filter
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
```

**WHY**: Functions are reusable blocks. Lambda is for quick, one-time operations.

---

## 5. ERROR HANDLING

### Try/Except/Finally
```python
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        print("Division attempt completed")  # Always runs

divide(10, 2)   # 5.0 → "Division attempt completed"
divide(10, 0)   # None → "Cannot divide by zero!" → "Division attempt completed"
```

### Raising Exceptions
```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return True

validate_age(28)   # True
validate_age(-5)   # ValueError: Age cannot be negative
```

**WHY**: Error handling prevents crashes. Raises exceptions for invalid data.

---

## 6. WORKING WITH FILES

### Read/Write Text
```python
# Write
with open('data.txt', 'w') as file:
    file.write("Hello, World!\n")
    file.write("Line 2\n")

# Read all at once
with open('data.txt', 'r') as file:
    content = file.read()  # Entire file as one string

# Read line by line
with open('data.txt', 'r') as file:
    for line in file:
        print(line.strip())  # strip() removes \n

# Read as list of lines
with open('data.txt', 'r') as file:
    lines = file.readlines()  # ['Hello, World!\n', 'Line 2\n']
```

### Work with JSON
```python
import json

# Write dict to JSON file
data = {'name': 'Phil', 'age': 28, 'skills': ['Python', 'SQL']}
with open('data.json', 'w') as file:
    json.dump(data, file, indent=2)

# Read JSON file back to dict
with open('data.json', 'r') as file:
    loaded_data = json.load(file)
    print(loaded_data['name'])  # 'Phil'

# String to dict
json_string = '{"name": "Phil", "age": 28}'
data = json.loads(json_string)

# Dict to string
json_string = json.dumps(data, indent=2)
```

**WHY**: Files are how data pipelines read input and write output. JSON is the standard for APIs.

---

## 7. COMMON PATTERNS FOR DATA WORK

### Filtering Data
```python
# Bad way (too much typing)
result = []
for item in items:
    if item['status'] == 'active' and item['age'] > 25:
        result.append(item)

# Good way (list comprehension)
result = [item for item in items if item['status'] == 'active' and item['age'] > 25]

# Even better (named for clarity)
active_adults = [
    person for person in people 
    if person['status'] == 'active' and person['age'] > 25
]
```

### Aggregating Data
```python
# Count occurrences
from collections import Counter

colors = ['red', 'blue', 'red', 'green', 'blue', 'red']
counts = Counter(colors)  # Counter({'red': 3, 'blue': 2, 'green': 1})

# Group by key
transactions = [
    {'user': 'alice', 'amount': 100},
    {'user': 'bob', 'amount': 50},
    {'user': 'alice', 'amount': 75},
]

from itertools import groupby
from operator import itemgetter

# Sort first (groupby requires sorted data)
sorted_transactions = sorted(transactions, key=itemgetter('user'))
grouped = {}
for user, group in groupby(sorted_transactions, key=itemgetter('user')):
    grouped[user] = [t['amount'] for t in group]
# grouped = {'alice': [100, 75], 'bob': [50]}
```

### Sorting
```python
# Sort list of primitives
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_numbers = sorted(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]
reversed_sort = sorted(numbers, reverse=True)  # [9, 6, 5, 4, 3, 2, 1, 1]

# Sort list of dicts
people = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
    {'name': 'Charlie', 'age': 35},
]
sorted_by_age = sorted(people, key=lambda x: x['age'])
sorted_by_name = sorted(people, key=lambda x: x['name'])
```

**WHY**: These patterns are 80% of data engineering work.

---

## 8. MODULES & IMPORTS

### Standard Library
```python
import math
math.sqrt(16)  # 4.0

from datetime import datetime
now = datetime.now()
print(now.year, now.month, now.day)

from collections import defaultdict
d = defaultdict(list)
d['fruits'].append('apple')  # Works without pre-creating 'fruits' key

import random
random.choice([1, 2, 3, 4, 5])  # Random element
random.shuffle(my_list)  # Shuffle in place
```

### Third-Party Libraries (You'll Use)
```python
# Pandas (data manipulation)
import pandas as pd
df = pd.read_csv('data.csv')

# Requests (HTTP)
import requests
response = requests.get('https://api.example.com/data')
data = response.json()

# SQLAlchemy (database)
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:password@localhost/dbname')
```

**WHY**: You don't write everything from scratch—you import what exists.

---

## 9. STRING OPERATIONS (QUICK REFERENCE)

```python
name = "Phil Dinh"

# Case
upper = name.upper()  # "PHIL DINH"
lower = name.lower()  # "phil dinh"

# Split/Join
parts = name.split()  # ['Phil', 'Dinh']
joined = '-'.join(parts)  # 'Phil-Dinh'

# Strip whitespace
messy = "  hello  "
clean = messy.strip()  # "hello"

# Find/Replace
message = "Hello, World!"
index = message.find("World")  # 7
replaced = message.replace("World", "Python")  # "Hello, Python!"

# Check if substring exists
"Phil" in name  # True

# F-strings (modern, use this)
age = 28
greeting = f"I am {age} years old"  # "I am 28 years old"

# String formatting (older, know it exists)
greeting = "I am {} years old".format(age)
```

**WHY**: You manipulate strings constantly in data pipelines.

---

## 10. COMMON PITFALLS & HOW TO AVOID THEM

### Mutable Default Arguments (TRAP!)
```python
# BAD: The list is created once and reused
def add_item(item, items=[]):
    items.append(item)
    return items

add_item(1)  # [1]
add_item(2)  # [1, 2] — OOPS, 1 is still there!

# GOOD: Create new list each time
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

add_item(1)  # [1]
add_item(2)  # [2]
```

### Off-by-One Errors with Range
```python
# range(5) gives 0, 1, 2, 3, 4 (NOT 5)
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Slicing: [start:stop) means stop is NOT included
my_list = [0, 1, 2, 3, 4]
my_list[1:3]  # [1, 2] (NOT including 3)
```

### Modifying List While Iterating (TRAP!)
```python
# BAD: This skips elements
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Oops!

# GOOD: Iterate over a copy or use list comprehension
numbers = [x for x in numbers if x % 2 != 0]
```

### Forgetting Return Value
```python
# BAD: Function doesn't return anything
def process_data(data):
    data = data.upper()
    # Oops, forgot return!

result = process_data("hello")  # None, not "HELLO"

# GOOD:
def process_data(data):
    data = data.upper()
    return data
```

---

## HOW TO USE THIS GUIDE

1. **Read one section at a time**
2. **Copy-paste examples into a Python file** (create `practice.py`)
3. **Run them**: `python practice.py`
4. **Modify them**: Change values, see what breaks
5. **Ask yourself**: "WHY does this work? What would happen if I...?"

---

## Next Steps

Once you've reviewed this guide:
- Open your portfolio projects and **read your own code** line by line
- Ask yourself: "Could I explain this to an interviewer in 30 seconds?"
- If you can't, that's a red flag—review that section again

You've got this! 💪
