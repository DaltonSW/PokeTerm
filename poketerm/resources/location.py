from poketerm.resources.data import AbstractData
from poketerm.console import console


class Location(AbstractData):
    MAX_COUNT = 867
    ENDPOINT = "location"
    VALID_NAMES = set()
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}

    def __init__(self, data):
        super().__init__(data)

        self.areas = []
        for area in data.get("areas"):
            self.areas.append(area.get("name"))

        self.region = data.get("region").get("name")

    def PrintData(self):
        console.clear()
        return

    def AddToCache(self):
        super().AddToCache()
