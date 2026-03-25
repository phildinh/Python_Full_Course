import pytest
from pipeline import extract_character_fields, filter_alive_characters, transform_batch

# ---- extract_character_fields() ----

def test_extract_returns_correct_fields():
    raw = {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human",
        "gender": "Male",          # field we don't want
        "image": "rick.jpeg"       # field we don't want
    }
    result = extract_character_fields(raw)
    assert result == {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "alive",
        "species": "human",
        "is_alive": True
    }

def test_extract_normalises_status_to_lowercase():
    raw = {
        "id": 2,
        "name": "Test",
        "status": "Dead",
        "species": "Human"
    }
    result = extract_character_fields(raw)
    assert result["status"] == "dead"
    assert result["is_alive"] == False

def test_extract_missing_field_raises_error():
    raw = {"id": 1, "name": "Test"}   # missing status and species
    with pytest.raises(KeyError):
        extract_character_fields(raw)

# ---- filter_alive_characters() ----

def test_filter_returns_only_alive():
    characters = [
        {"name": "Rick", "is_alive": True},
        {"name": "Dead guy", "is_alive": False},
        {"name": "Morty", "is_alive": True}
    ]
    result = filter_alive_characters(characters)
    assert len(result) == 2
    assert all(c["is_alive"] for c in result)

def test_filter_empty_list_returns_empty():
    assert filter_alive_characters([]) == []

def test_filter_all_dead_returns_empty():
    characters = [
        {"name": "Dead guy", "is_alive": False},
        {"name": "Also dead", "is_alive": False}
    ]
    assert filter_alive_characters(characters) == []

# ---- transform_batch() ----

def test_transform_batch_returns_only_alive_cleaned_records():
    raw_characters = [
        {"id": 1, "name": "Rick Sanchez", "status": "Alive", "species": "Human"},
        {"id": 2, "name": "Dead guy",     "status": "Dead",  "species": "Alien"},
        {"id": 3, "name": "Morty Smith",  "status": "Alive", "species": "Human"}
    ]
    result = transform_batch(raw_characters)
    assert len(result) == 2
    assert result[0]["name"] == "Rick Sanchez"
    assert result[1]["name"] == "Morty Smith"
    assert all(c["is_alive"] for c in result)

def test_transform_batch_empty_input():
    assert transform_batch([]) == []