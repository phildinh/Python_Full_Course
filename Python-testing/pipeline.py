def extract_character_fields(raw_character):
    """
    Takes a raw character dict from the Rick and Morty API
    and returns only the fields we want to load into the database
    """
    return {
        "id": raw_character["id"],
        "name": raw_character["name"],
        "status": raw_character["status"].lower(),        # normalise to lowercase
        "species": raw_character["species"].lower(),      # normalise to lowercase
        "is_alive": raw_character["status"] == "Alive"   # convert to boolean
    }

def filter_alive_characters(characters):
    """Returns only characters that are alive"""
    return [c for c in characters if c["is_alive"]]

def transform_batch(raw_characters):
    """
    Takes a list of raw API characters
    and returns cleaned records ready for the database
    """
    extracted = [extract_character_fields(c) for c in raw_characters]
    return filter_alive_characters(extracted)