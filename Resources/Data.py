from abc import ABC, abstractmethod
import re
import Utils

class AbstractData(ABC):
    ENDPOINT = None
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}

    @abstractmethod
    def __init__(self, data):
        self.ID: int = data['id']
        self.name: str = data['name']
        self.ID_TO_NAME_CACHE[self.ID] = self.name

    @abstractmethod
    def PrintData(self):
        pass

    @abstractmethod
    def AddToCache(self):
        self.ID_TO_NAME_CACHE[self.ID] = self.name
        self.NAME_TO_DATA_CACHE[self.name] = self

    @classmethod
    def LoadCache(cls):
        data = Utils.LoadCache(cls.ENDPOINT)
        try:
            cls.ID_TO_NAME_CACHE, cls.NAME_TO_DATA_CACHE = data
        except TypeError:
            print(f"Failed to load {cls.ENDPOINT.upper()} cache")
            pass

    @classmethod
    def SaveCache(cls):
        if len(cls.NAME_TO_DATA_CACHE) == 0:
            return
        output = (cls.ID_TO_NAME_CACHE, cls.NAME_TO_DATA_CACHE)
        Utils.SaveCache(cls.ENDPOINT, output)

    @classmethod
    def HandleSearch(cls, query=None):
        if query is None:
            query = input(f'{cls.ENDPOINT.title()} Name or ID: ').lower()
        if query.isdigit():
            query = Utils.ProperQueryFromID(int(query), cls.ID_TO_NAME_CACHE)
        if query in cls.NAME_TO_DATA_CACHE:
            return cls.NAME_TO_DATA_CACHE[query]
        data = Utils.GetFromAPI(cls.ENDPOINT, query)
        if data is not None:
            newObject = cls(data)
            cls.NAME_TO_DATA_CACHE[newObject.name] = newObject
            return newObject

    @property
    def PrintName(self) -> str:
        self.name = re.sub('-', ' ', self.name)
        return self.name.title()
