from poketerm.resources.data import AbstractData
from poketerm.console import console
import poketerm.utils as utils


class EggGroup(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = "egg-group"

    def __init__(self, data):
        super().__init__(data)

        self.pokemon = data["pokemon_species"]

    def PrintData(self):
        utils.ClearScreen()

        console.rule(f"Egg Group: {self.PrintName}", style="")
        print()
        console.print(f"Pokemon in this egg group:")

        for pokemon in self.pokemon:
            console.print(pokemon.get("name").title())

        return

    def AddToCache(self):
        super().AddToCache()
