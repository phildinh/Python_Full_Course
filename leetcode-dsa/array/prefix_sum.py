sales = [100, 200, 300, 400, 500, 600, 700]

def range_sum(sales,left,right):
    total = 0
    for i in range(left,right + 1):
        total += sales[i]
    return total

print(range_sum(sales, 1, 4))   # day 2 to day 5
print(range_sum(sales, 0, 3))   # day 1 to day 4
print(range_sum(sales, 2, 6))   # day 3 to day 7

# Better way
sales = [100, 200, 300, 400, 500, 600, 700]

# Step 1 — build prefix sum array once — O(n)
prefix = [0] * (len(sales) + 1)       # one extra slot at the start

for i in range(len(sales)):
    prefix[i + 1] = prefix[i] + sales[i]

print(prefix)
# [0, 100, 300, 600, 1000, 1500, 2100, 2800]
# ↑ extra 0 at start makes the subtraction formula clean

# Step 2 — answer any range query instantly — O(1)
def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]

print(range_sum(prefix, 1, 4))   # day 2 to day 5 = 1400
print(range_sum(prefix, 0, 3))   # day 1 to day 4 = 1000
print(range_sum(prefix, 2, 6))   # day 3 to day 7 = 2200