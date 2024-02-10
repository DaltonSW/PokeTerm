import re
import asyncio
import aiohttp
from typing import Optional

from poketerm.utils.api import get_from_API, get_from_API_async
from poketerm.utils.caching import CacheManager
from poketerm.resources.data import Resource


class SearchManager:
    VALID_NAMES: dict[str, list[str]] = {}

    @classmethod
    def update_valid_names(cls, resource):
        if resource.ENDPOINT not in cls.VALID_NAMES:
            cls.VALID_NAMES[resource.ENDPOINT] = []
        if resource.name not in cls.VALID_NAMES[resource.ENDPOINT]:
            cls.VALID_NAMES[resource.ENDPOINT].append(resource.name)

    @classmethod
    def load_valid_names(cls, searchable_resources: list[Resource]) -> None:
        cache = CacheManager.load_cache_of_type("valid-names")
        if cache:
            cls.VALID_NAMES = cache
            return
        for resource in searchable_resources:
            names = []
            for i in range(1, resource.MAX_COUNT + 1):
                res = cls.handle_search_and_cast(resource, i)
                names.append(res.name)

            cls.VALID_NAMES[resource.ENDPOINT] = names

        cls.save_valid_names()
        return

    @classmethod
    def save_valid_names(cls):
        CacheManager.save_cache_of_type("valid-names", cls.VALID_NAMES)

    @classmethod
    def handle_search_and_cast(cls, resource, query: Optional[str | int] = None):
        data = SearchManager.handle_search(resource.ENDPOINT, query)

        if data is None:
            return

        if isinstance(data, Resource):
            resource = data
        else:  # This creates an instance of search_resource based on the queried data
            resource = resource(data)
        return resource

    @classmethod
    def handle_search(cls, endpoint: str, query: Optional[str | int] = None):
        if query is None or query == "":
            q = prompt_for_query(endpoint)
            if q == "":
                return
        else:
            q = str(query)

        q = normalize_search_term(q)
        data = obtain_data(endpoint, q)

        if data is None:
            # print("oops no data!")
            # TODO: Implement fuzzy-finding
            return
        return data


def obtain_data(endpoint: str, query: str):
    if query.isdigit():
        data = CacheManager.get_data_from_ID(endpoint, query)
    else:
        data = CacheManager.get_data_from_name(endpoint, query)

    if data:
        return data

    return get_from_API(endpoint, query)


async def obtain_data_async(endpoint: str, query: str, session):
    if query.isdigit():
        data = CacheManager.get_data_from_ID(endpoint, query)
    else:
        data = CacheManager.get_data_from_name(endpoint, query)

    if data:
        return data

    data = await get_from_API_async(endpoint, query, session)


def prompt_for_query(endpoint: str):
    return input(f"{endpoint.title()} Name or ID: ").lower()


def normalize_search_term(searchTerm: str) -> str:
    return re.sub(" ", "-", searchTerm)
