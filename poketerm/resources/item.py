from poketerm.resources.data import AbstractData
from poketerm.console import console


class Item(AbstractData):
    MAX_COUNT = 2159
    ENDPOINT = "item"
    VALID_NAMES = set()
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}

    def __init__(self, data):
        super().__init__(data)

    def PrintData(self):
        console.clear()
        return

    def AddToCache(self):
        super().AddToCache()
