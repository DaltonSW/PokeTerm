import requests

BASE_URL = "https://pokeapi.co/api/v2"


def GetIDFromURL(URL: str) -> int:
    return int(URL.split("/")[-2])


def get_from_api(endpoint, searchTerm):
    response = requests.get(f"{BASE_URL}/{endpoint}/{searchTerm}")
    if response.status_code == 404:
        return None
    return response.json()


# If the int being searched on is in the id->name cache, return the proper name. Otherwise, return the original param
def ProperQueryFromID(query: int, idToNameCache) -> str | int:
    return query if query not in idToNameCache else idToNameCache[query]


def GetFromURL(url) -> dict | None:
    response = requests.get(url)
    if response.status_code == 404:
        return None
    return response.json()
