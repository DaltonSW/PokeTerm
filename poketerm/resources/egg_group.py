from poketerm.resources.data import Resource
from poketerm.console import console
from poketerm.utils.visual import ClearScreen


class EggGroup(Resource):
    ENDPOINT = "egg-group"

    def __init__(self, data):
        super().__init__(data)

        self.pokemon = data["pokemon_species"]

    def print_data(self):
        ClearScreen()

        console.rule(f"Egg Group: {self.PrintName}", style="")
        print()
        console.print(f"Pokemon in this egg group:")

        for pokemon in self.pokemon:
            console.print(pokemon.get("name").title())

        return
