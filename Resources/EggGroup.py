from rich.table import Table

from .Data import AbstractData
from console import console
import Utils


class EggGroup(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = "egg-group"

    def __init__(self, data):
        super().__init__(data)

        self.pokemon = data["pokemon_species"]

    def PrintData(self):
        Utils.ClearScreen()

        console.rule(f"Egg Group: {self.PrintName}", style="")
        print()
        console.print(f"Pokemon in this egg group:")

        for pokemon in self.pokemon:
            console.print(pokemon.get("name").title())

        return

    def AddToCache(self):
        super().AddToCache()
