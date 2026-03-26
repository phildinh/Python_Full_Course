sales = [
    {"sale_id": 1, "store": "Sydney CBD",  "amount": 250},
    {"sale_id": 2, "store": "Parramatta",  "amount": 80},
    {"sale_id": 3, "store": "Chatswood",   "amount": 430},
    {"sale_id": 4, "store": "Sydney CBD",  "amount": 120},
    {"sale_id": 5, "store": "Parramatta",  "amount": 95},
]

store_regions = [
    {"store": "Sydney CBD",  "region": "Metro"},
    {"store": "Parramatta",  "region": "Western"},
    {"store": "Chatswood",   "region": "Northern"},
]

nested_loop = []
for sale in sales:
    for store in store_regions:
        if sale["store"] == store["store"]:
            nested_loop.append({
                "sale_id": sale["sale_id"],
                "store": sale["store"],
                "region": store["region"],
                "amount": sale["amount"]
            })

print(nested_loop)

# goodway:
region_lookup = {
    t["store"]: t["region"] for t in store_regions
}

nested = []

for sale in sales:
    region = region_lookup.get(sale["store"])

    if region:
        nested.append({
                "sale_id": sale["sale_id"],
                "store": sale["store"],
                "region": region,
                "amount": sale["amount"]  
        })

print(nested)