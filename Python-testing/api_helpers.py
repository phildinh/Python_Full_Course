import requests

def get_character(character_id):
    """Fetches a single character from the Rick and Morty API"""
    response = requests.get(
        url = f"https://rickandmortyapi.com/api/character/{character_id}",
        timeout=10
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id": data["id"],
        "name": data["name"],
        "status": data["status"]
    } 