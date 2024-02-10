from poketerm.resources.data import Resource
from poketerm.console import console
from poketerm.utils.visual import clear_screen


class EggGroup(Resource):
    MAX_COUNT = 15
    ENDPOINT = "egg-group"

    def __init__(self, data):
        super().__init__(data)

        self.pokemon = data["pokemon_species"]

    def print_data(self):
        clear_screen()

        console.rule(f"Egg Group: {self.print_name}", style="")
        print()
        console.print(f"Pokemon in this egg group:")

        for pokemon in self.pokemon:
            console.print(pokemon.get("name").title())

        return
