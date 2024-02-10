import requests

BASE_URL = "https://pokeapi.co/api/v2"


def get_ID_from_URL(URL: str) -> int:
    return int(URL.split("/")[-2])


def get_from_API(endpoint, searchTerm):
    response = requests.get(f"{BASE_URL}/{endpoint}/{searchTerm}")
    if response.status_code == 404:
        return None
    return response.json()


def get_from_URL(url) -> dict | None:
    response = requests.get(url)
    if response.status_code == 404:
        return None
    return response.json()
