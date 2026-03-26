from etl import clean_order, clean_batch
import pytest

valid_order_1 = {
    "order_id": "ORD-001",
    "customer_name": "John Smith",
    "amount": "$1,250.99",
    "status": "COMPLETED"
}

valid_order_2 = {
    "order_id": "ORD-002",
    "customer_name": "Jane Doe",
    "amount": "$500.00",
    "status": "PENDING"
}

bad_order = {
    "order_id": "ORD-003",
    "customer_name": "Bob",
    "amount": "N/A",
    "status": "COMPLETED"
}

raw_order = {
    "order_id": "ORD-001",
    "customer_name": "  John Smith  ",
    "amount": "$1,250.99",
    "status": "COMPLETED",
    "product_id": 42,
    "internal_ref": "xyz-internal"
}

def test_clean_order_returns_correct_output():
    result = clean_order(raw_order)
    assert result == {
        "order_id": "ORD-001",
        "customer_name": "John Smith",
        "amount": 1250.99,
        "status": "completed"
    }

# order A — blank customer name
def test_clean_order_blank_customer_name():
    blank_name_order = {
        "order_id": "ORD-002",
        "customer_name": "  ",        # only whitespace
        "amount": "$0.00",
        "status": "COMPLETED" 
    }
    result = clean_order(blank_name_order)
    assert result["customer_name"] == ""

# order B — "N/A" amount, expect ValueError
def test_clean_order_invalid_amount():
    invalid_amount_order = {
        "order_id": "ORD-003",
        "customer_name": "Jane Doe", 
        "amount": "N/A", 
        "status": "COMPLETED"
    }
    with pytest.raises(ValueError):
        clean_order(invalid_amount_order)
        

# order C — missing amount key, expect KeyError
def test_clean_order_missing_amount_key():
    missing_key_order = {
        "order_id": "ORD-004", 
        "customer_name": "Bob", 
        "status": "COMPLETED"
    }
    with pytest.raises(KeyError):
        clean_order(missing_key_order)

# now write the three tests
def test_clean_batch_all_valid():
    result = clean_batch([valid_order_1, valid_order_2])
    assert len(result) == 2
    assert result[0]["order_id"] == "ORD-001"
    assert result[1]["order_id"] == "ORD-002"

def test_clean_batch_one_bad_order():
    result = clean_batch([valid_order_1, bad_order])
    assert len(result) == 1                          # only valid_order_1 came through
    assert result[0]["order_id"] == "ORD-001"        # bad_order was skipped

def test_clean_batch_all_bad():
    result = clean_batch([bad_order])
    assert result == []                              # nothing came through