import requests

BASE_URL = "https://pokeapi.co/api/v2"
LOCAL_URL = "http://localhost/api/v2"


def get_ID_from_URL(URL: str) -> int:
    return int(URL.split("/")[-2])


def get_from_API(endpoint, searchTerm):
    from poketerm.utils.testing import TEST_RUNNING

    response = requests.get(
        f"{LOCAL_URL if TEST_RUNNING else BASE_URL}/{endpoint}/{searchTerm}"
    )
    if response.status_code == 404:
        return None
    return response.json()


async def get_from_API_async(endpoint, searchTerm, session):
    from poketerm.utils.testing import TEST_RUNNING

    async with session.get(
        f"{LOCAL_URL if TEST_RUNNING else BASE_URL}/{endpoint}/{searchTerm}"
    ) as response:
        resp = await response
    if resp.status_code == 404:
        return None
    return resp.json()


def get_from_URL(url) -> dict | None:
    response = requests.get(url)
    if response.status_code == 404:
        return None
    return response.json()
