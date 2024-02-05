from poketerm.resources.data import Resource
from poketerm.console import console


class Encounter(Resource):
    ENDPOINT = "encounter"

    def __init__(self, data):
        super().__init__(data)

    def print_data(self):
        console.clear()
        return
