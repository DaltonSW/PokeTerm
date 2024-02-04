from poketerm.resources.data import Resource
from poketerm.console import console


class Item(Resource):
    MAX_COUNT = 2159
    ENDPOINT = "item"
    VALID_NAMES = set()
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}

    def __init__(self, data):
        super().__init__(data)

    def print_data(self):
        console.clear()
        return

    def AddToCache(self):
        super().AddToCache()
