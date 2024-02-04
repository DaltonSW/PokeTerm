import re
from abc import ABC, abstractmethod
from poketerm.utils.caching import CacheManager


class Resource(ABC):
    ENDPOINT = None
    MAX_COUNT = -1
    VALID_NAMES = set()

    @abstractmethod
    def __init__(self, data):
        self.ID: int = data.get("id")
        self.name: str = data.get("name")
        CacheManager.add_name_to_ID_mapping(self.ENDPOINT, self.name, self.ID)

    @abstractmethod
    def print_data(self):
        pass

    @classmethod
    def ToggleFlag(cls, flag: str):
        pass

    @property
    def PrintName(self) -> str:
        self.name = re.sub("-", " ", self.name)
        return self.name.title()
