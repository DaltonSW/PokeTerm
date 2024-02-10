import re

from readchar import readkey
from thefuzz import process
from typing import Optional

from poketerm.utils.api import get_from_API, get_from_API_async
from poketerm.utils.caching import CacheManager
from poketerm.resources.data import Resource
from poketerm.console import console


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
                return None
        else:
            q = str(query)

        q = normalize_search_term(q)
        data = obtain_data(endpoint, q)

        if data is None:
            choices = process.extract(q, cls.VALID_NAMES[endpoint])
            for i, choice in enumerate(choices):
                console.print(f"[{i + 1}] {choice[0]}")
            console.print(
                "Query not found! [1-5] for closest matches, or anything else to return."
            )
            key = readkey()
            if key.isdigit() and 5 >= int(key) > 0:
                return obtain_data(endpoint, choices[int(key) - 1][0])
            return None
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
    return data


def prompt_for_query(endpoint: str):
    return input(f"{endpoint.title()} Name or ID: ").lower()


def normalize_search_term(searchTerm: str) -> str:
    return re.sub(" ", "-", searchTerm)
