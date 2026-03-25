def add (a,b):
    return a + b

def divide(a,b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a/b

def multiply(a,b):
    return a * b

def clean_amount(value):
    """Strips $ sign and converts to float — like cleaning order amounts from an API"""
    return float(value.replace("$","").replace(",",""))