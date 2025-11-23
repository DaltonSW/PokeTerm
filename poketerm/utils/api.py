import asyncio
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

BASE_URL = "https://pokeapi.co/api/v2"
LOCAL_URL = "http://localhost/api/v2"
REQUEST_TIMEOUT = 10  # seconds


def get_ID_from_URL(URL: str) -> int:
    return int(URL.split("/")[-2])


def get_from_API(endpoint, searchTerm):
    from poketerm.utils.testing import TEST_RUNNING

    try:
        response = requests.get(
            f"{LOCAL_URL if TEST_RUNNING else BASE_URL}/{endpoint}/{searchTerm}",
            timeout=REQUEST_TIMEOUT
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except (Timeout, ConnectionError) as e:
        # Handle timeout and connection errors gracefully
        return None
    except RequestException as e:
        # Handle other request exceptions
        return None


async def get_from_API_async(endpoint, searchTerm, session):
    import aiohttp
    from poketerm.utils.testing import TEST_RUNNING

    try:
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        async with session.get(
            f"{LOCAL_URL if TEST_RUNNING else BASE_URL}/{endpoint}/{searchTerm}",
            timeout=timeout
        ) as response:
            if response.status == 404:
                return None
            response.raise_for_status()
            return await response.json()
    except (aiohttp.ClientError, asyncio.TimeoutError):
        # Handle timeout and connection errors gracefully
        return None


def get_from_URL(url) -> dict | None:
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except (Timeout, ConnectionError, RequestException):
        return None
