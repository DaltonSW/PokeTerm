from poketerm.resources.data import Resource
from poketerm.console import console


class GrowthRate(Resource):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = "growth-rate"

    def __init__(self, data):
        super().__init__(data)
        self.formula = data.get("formula")

        self.levels = {}
        for thing in data.get("levels"):
            self.levels[thing.get("level")] = thing.get("experience")

        self.species = []
        for thing in data.get("pokemon_species"):
            self.species.append(thing.get("name"))

    def print_data(self):
        console.clear()
        return

    def AddToCache(self):
        super().AddToCache()
