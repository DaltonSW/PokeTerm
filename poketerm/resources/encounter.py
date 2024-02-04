from poketerm.resources.data import Resource
from poketerm.console import console


class Encounter(Resource):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = "encounter"

    def __init__(self, data):
        super().__init__(data)

    def print_data(self):
        console.clear()
        return

    def AddToCache(self):
        super().AddToCache()
