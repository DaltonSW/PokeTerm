from poketerm.resources.data import AbstractData
from poketerm.console import console


class Location(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = "location"

    def __init__(self, data):
        super().__init__(data)

    def PrintData(self):
        console.clear()
        return

    def AddToCache(self):
        super().AddToCache()
