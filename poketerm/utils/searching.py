import re
from typing import Optional

from poketerm.utils.api import get_from_api
from poketerm.utils.caching import CacheManager


class SearchManager:
    VALID_NAMES: dict[str, list[str]] = []

    @classmethod
    def handle_search(cls, endpoint: str, query: Optional[str] = None):
        if query is None or query == "":
            q = prompt_for_query(endpoint)
            if q == "":
                return
        else:
            q = query

        q = normalize_search_term(q)
        data = obtain_data(endpoint, q)

        if data is None:
            print("oops no data!")
            # TODO: Implement fuzzy-finding
            return
        input()


def obtain_data(endpoint: str, query: str):
    if query.isdigit():
        data = CacheManager.get_data_from_ID(endpoint, query)
    else:
        data = CacheManager.get_data_from_name(endpoint, query)

    if data:
        return data

    return get_from_api(endpoint, query)


def prompt_for_query(endpoint: str):
    return input(f"{endpoint.title()} Name or ID: ").lower()


def normalize_search_term(searchTerm: str) -> str:
    return re.sub(" ", "-", searchTerm)
