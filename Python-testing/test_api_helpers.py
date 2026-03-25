from unittest.mock import patch, MagicMock
from api_helpers import get_character
import requests
import pytest

def test_get_character_returns_correct_fields():
    # 1. build the fake response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id":1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human"
    }
    mock_response.raise_for_status.return_value = None

    # 2. patch requests.get to return our fake response
    with patch("api_helpers.requests.get", return_value = mock_response):
        result = get_character(1)

    # 3. assert the output
    assert result["id"] == 1
    assert result["name"] == "Rick Sanchez"
    assert result["status"] == "Alive"

def test_get_character_raises_on_bad_status():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("api_helpers.requests.get", return_value = mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            get_character(999)

def test_get_character_raises_connection_erorr():
     with patch("api_helpers.requests.get", side_effect = requests.exceptions.ConnectionError):
        with pytest.raises(requests.exceptions.ConnectionError):
            get_character(1)