from poketerm.resources.data import AbstractData
from poketerm.console import console


class Region(AbstractData):
    MAX_COUNT = 10
    ENDPOINT = "region"
    VALID_NAMES = set()
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}

    def __init__(self, data):
        super().__init__(data)

        self.locations = []
        for location in data.get("locations"):
            self.locations.append(location.get("name"))

        main_gen = data.get("main_generation")
        if main_gen:
            self.main_generation = main_gen.get("name")

        self.pokedexes = []
        for pokedex in data.get("pokedexes"):
            self.pokedexes.append(pokedex.get("name"))

        self.version_groups = []
        for group in data.get("version_groups"):
            self.pokedexes.append(group.get("name"))

    def PrintData(self):
        console.clear()
        return

    def AddToCache(self):
        super().AddToCache()
