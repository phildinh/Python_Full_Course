temps = [-10, -3, 0, 5, 12, 18, 24]

# Normal way will get big time complexity O(n*n)
for i in range(len(temps)):
    for j in range(i+1, len(temps)):
        if temps[i] + temps[j] == 14:
            print(temps[i],temps[j])

# better way to reduce time complexity

left = 0
right = int(len(temps) - 1)

while left < right:
    if temps[left] + temps[right] < 14:
        left += 1
    elif temps[left] + temps[right] > 14:
        right -= 1
    if temps[left] + temps[right] == 14:
        print(temps[left],temps[right])
        break

deliveries = [10, 25, 40, 70, 85, 100, 130]
target_gap = 15

left = 0
right = 1

while right < len(deliveries):
    gap = deliveries[right] - deliveries[left]
    if gap == target_gap:
        print(f"Match: {deliveries[left]} and {deliveries[right]}")
        left += 1
        right += 1

    elif gap < target_gap:
        right += 1

    elif gap > target_gap:
        left += 1