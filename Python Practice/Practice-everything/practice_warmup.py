"""
PYTHON WARM-UP PRACTICE
Run this file: python practice_warmup.py
Modify and experiment with each section
"""

print("=" * 60)
print("SECTION 1: DATA STRUCTURES")
print("=" * 60)

# Lists
my_list = [1, 2, 3, 4, 5]
print(f"List: {my_list}")
print(f"First element: {my_list[0]}")
print(f"Last element: {my_list[-1]}")
print(f"Slice [1:3]: {my_list[1:3]}")

# Dictionaries
person = {'name': 'Phil', 'age': 28, 'city': 'Sydney'}
print(f"\nDict: {person}")
print(f"Name: {person['name']}")
print(f"Age: {person.get('age')}")

# Sets
colors = {'red', 'blue', 'green'}
print(f"\nSet: {colors}")
print(f"Is 'red' in colors? {'red' in colors}")

print("\n" + "=" * 60)
print("SECTION 2: LOOPS & ITERATION")
print("=" * 60)

# For loop with range
print("\nFor loop (range 5):")
for i in range(5):
    print(f"  i = {i}")

# For loop with enumerate
fruits = ['apple', 'banana', 'cherry']
print("\nFor loop with enumerate:")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

# Zip
names = ['Alice', 'Bob']
ages = [25, 30]
print("\nZip (combine lists):")
for name, age in zip(names, ages):
    print(f"  {name} is {age}")

print("\n" + "=" * 60)
print("SECTION 3: LIST COMPREHENSION")
print("=" * 60)

numbers = [1, 2, 3, 4, 5]

# Basic
squared = [x**2 for x in numbers]
print(f"Original: {numbers}")
print(f"Squared: {squared}")

# With condition
evens = [x for x in numbers if x % 2 == 0]
print(f"Evens only: {evens}")

# Combined
squared_evens = [x**2 for x in numbers if x % 2 == 0]
print(f"Squared evens: {squared_evens}")

print("\n" + "=" * 60)
print("SECTION 4: FUNCTIONS")
print("=" * 60)

def greet(name, greeting="Hello"):
    """Say hello to someone."""
    return f"{greeting}, {name}!"

print(f"greet('Phil'): {greet('Phil')}")
print(f"greet('Phil', 'Hi'): {greet('Phil', 'Hi')}")

# Lambda
square = lambda x: x**2
print(f"\nLambda - square(5): {square(5)}")

# Map & Filter
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Map (square): {squared}")
print(f"Filter (evens): {evens}")

print("\n" + "=" * 60)
print("SECTION 5: ERROR HANDLING")
print("=" * 60)

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except Exception as e:
        return f"Error: {e}"

print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")

print("\n" + "=" * 60)
print("SECTION 6: WORKING WITH DICTS (DATA PATTERN)")
print("=" * 60)

# Sample data
transactions = [
    {'user': 'alice', 'amount': 100},
    {'user': 'bob', 'amount': 50},
    {'user': 'alice', 'amount': 75},
]

print("Transactions:", transactions)

# Filter: only alice's
alice_transactions = [t for t in transactions if t['user'] == 'alice']
print(f"Alice's transactions: {alice_transactions}")

# Aggregate: sum by user
totals = {}
for t in transactions:
    user = t['user']
    if user not in totals:
        totals[user] = 0
    totals[user] += t['amount']
print(f"Totals by user: {totals}")

print("\n" + "=" * 60)
print("SECTION 7: STRINGS")
print("=" * 60)

text = "Hello, Python!"
print(f"Original: {text}")
print(f"Upper: {text.upper()}")
print(f"Lower: {text.lower()}")
print(f"Split: {text.split(',')}")

# F-strings
name = "Phil"
age = 28
print(f"\nF-string: My name is {name} and I'm {age} years old")

print("\n" + "=" * 60)
print("SECTION 8: COMMON PATTERNS")
print("=" * 60)

# Pattern 1: Filtering
print("\nPattern - Filter:")
all_people = [
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30},
    {'name': 'Charlie', 'age': 35},
]
over_25 = [p for p in all_people if p['age'] > 25]
print(f"People over 25: {over_25}")

# Pattern 2: Sorting
print("\nPattern - Sort:")
sorted_by_age = sorted(all_people, key=lambda x: x['age'])
print(f"Sorted by age: {sorted_by_age}")

# Pattern 3: Counting
from collections import Counter
print("\nPattern - Count:")
colors_list = ['red', 'blue', 'red', 'green', 'blue', 'red']
color_counts = Counter(colors_list)
print(f"Color counts: {dict(color_counts)}")

print("\n" + "=" * 60)
print("DONE! Now try modifying these examples.")
print("=" * 60)
