from poketerm.resources.data import Resource
from poketerm.console import console


class Item(Resource):
    MAX_COUNT = 2159
    ENDPOINT = "item"
    VALID_NAMES = set()

    def __init__(self, data):
        super().__init__(data)

    def print_data(self):
        console.clear()
        return
