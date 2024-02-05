from poketerm.resources.data import Resource
from poketerm.console import console


class PokemonForm(Resource):

    ENDPOINT = "pokemon-form"

    def __init__(self, data):
        super().__init__(data)

    def print_data(self):
        console.clear()
        return
