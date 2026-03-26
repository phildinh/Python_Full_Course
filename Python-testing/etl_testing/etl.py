def clean_order(raw_order):
    return {
        "order_id":         raw_order["order_id"],
        "customer_name":    raw_order["customer_name"].strip(),
        "amount":           float(raw_order["amount"].replace("$","").replace(",","")),
        "status":           raw_order["status"].lower()
    }

def clean_batch(raw_orders):
    """Cleans a list of raw orders — skips any that fail"""
    cleaned = []
    for order in raw_orders:
        try:
            cleaned.append(clean_order(order))
        except (ValueError, KeyError):
            print(f"Skipping bad order: {order.get('order_id', 'unknown')}")
    return cleaned

