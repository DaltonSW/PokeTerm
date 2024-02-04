import re
from readchar import readkey, key as keys
from thefuzz import process
from poketerm.console import console
from abc import ABC, abstractmethod
from poketerm.utils.caching import save_cache, load_cache
from poketerm.utils.api import ProperQueryFromID, get_from_api


class Resource(ABC):
    ENDPOINT = None
    MAX_COUNT = -1
    VALID_NAMES = set()
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}

    @abstractmethod
    def __init__(self, data):
        self.ID: int = data.get("id")
        self.name: str = data.get("name")
        self.ID_TO_NAME_CACHE[self.ID] = self.name

    @abstractmethod
    def print_data(self):
        pass

    @abstractmethod
    def AddToCache(self):
        self.ID_TO_NAME_CACHE[self.ID] = self.name
        self.NAME_TO_DATA_CACHE[self.name] = self

    @classmethod
    def ToggleFlag(cls, flag: str):
        pass

    @classmethod
    def LoadCache(cls):
        data = load_cache(cls.ENDPOINT)
        try:
            if len(data) == 3:
                cls.ID_TO_NAME_CACHE, cls.NAME_TO_DATA_CACHE, cls.VALID_NAMES = data
            else:
                cls.ID_TO_NAME_CACHE, cls.NAME_TO_DATA_CACHE = data
        except TypeError:
            print(f"Failed to load {cls.ENDPOINT.upper()} cache")
            pass

    @classmethod
    def SaveCache(cls):
        if len(cls.NAME_TO_DATA_CACHE) == 0:
            return
        output = (cls.ID_TO_NAME_CACHE, cls.NAME_TO_DATA_CACHE, cls.VALID_NAMES)
        save_cache(cls.ENDPOINT, output)

    @classmethod
    def HandleSearch(cls, query=None):
        if query is None or query == "":
            query = input(f"{cls.ENDPOINT.title()} Name or ID: ").lower()

        if query == "":
            return None
        query = str(query)
        if query.isdigit():
            query = ProperQueryFromID(int(query), cls.ID_TO_NAME_CACHE)
        if query in cls.NAME_TO_DATA_CACHE:
            return cls.NAME_TO_DATA_CACHE[query]
        data = get_from_api(cls.ENDPOINT, query)

        if data is not None:
            # print(f"Loaded {data.get('name')} from {cls.ENDPOINT} API")
            newObject = cls(data)
            cls.NAME_TO_DATA_CACHE[newObject.name] = newObject
            cls.VALID_NAMES.add(newObject.name)
            return newObject
        elif isinstance(query, str):
            results = process.extract(query, cls.VALID_NAMES)
            console.print(
                "Unable to find that search term. Here are the 5 closest matches: "
            )
            console.print(f"[1] {results[0][0]}")
            console.print(f"[2] {results[1][0]}")
            console.print(f"[3] {results[2][0]}")
            console.print(f"[4] {results[3][0]}")
            console.print(f"[5] {results[4][0]}")
            console.rule("Press [Enter] to return to the menu.", characters=" ")
            key = readkey()
            if key == keys.ENTER:
                return
            # TODO: Check the input key and print that data

    @property
    def PrintName(self) -> str:
        self.name = re.sub("-", " ", self.name)
        return self.name.title()
