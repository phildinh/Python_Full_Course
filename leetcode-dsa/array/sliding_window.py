sales = [100, 200, 300, 400, 500, 600, 700]
k = 3   # window size — number of consecutive days

best = 0

for i in range(len(sales) - k + 1):
    print(i)
    total = 0
    for j in range(i, i + k):
        print(i,j)
        total += sales[j]
    if total > best:
        best = total
    
print(best)

# Reduce time complexity
sales = [100, 200, 300, 400, 500, 600, 700]
k = 3

# Step 1 - calculate first window sum
window_sum = sum(sales[0:k])
best_sum = window_sum
best_start = 0

# Step 2 - slide the window forward
for i in range(1, len(sales) -k + 1):
    window_sum = window_sum - sales[i - 1] + sales[i + k - 1]

    if window_sum > best_sum:
        best_sum = window_sum
        best_start = i

print(f"Best 3 days: {sales[best_start: best_start + k]}")
print(f"Total: {best_sum}")

sales_2 = [200, 100, 400, 300, 500, 250, 350]
k = 3

window_sum = sum(sales_2[0:k])
best_sum = window_sum
best_start = 0

for i in range(1, len(sales_2) -k + 1):
    window_sum = window_sum - sales_2[i -1] + sales_2[i + 3 -1]
    
    if window_sum > best_sum:
        best_sum = window_sum
        best_start = i

print(f"Best 3 days: {sales_2[best_start: best_start + k]}")
print(f"Total: {best_sum}")