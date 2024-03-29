from typing import Optional

from poketerm.resources.data import Resource
from poketerm.console import console


class Pokedex(Resource):
    MAX_COUNT = 33
    ENDPOINT = "pokedex"
    VALID_NAMES = set()

    def __init__(self, data):
        super().__init__(data)

        self.is_main_series = data.get("is_main_series")

        self.region: Optional[str] = data.get("region")

        self.pokemon_entries = {}
        pokemon_data = data.get("pokemon_entries")
        if pokemon_data:
            for entry in pokemon_data:
                pokemon_id = entry.get("entry_number")
                pokemon_name = entry.get("pokemon_species").get("name")
                self.pokemon_entries[pokemon_id] = pokemon_name

        self.version_groups = []
        for group in data.get("version_groups"):
            self.version_groups.append(group.get("name"))

    def print_data(self):
        console.clear()
        return
