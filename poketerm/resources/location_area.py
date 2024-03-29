from poketerm.resources.data import Resource
from poketerm.console import console


class LocationArea(Resource):

    ENDPOINT = "location-area"

    def __init__(self, data):
        super().__init__(data)

        self.location = data.get("location").get("name")
        self.game_index = data.get("game_index")

        encounter_data = data.get("pokemon_encounters")

        self.encounters = {}
        for poke in encounter_data:
            poke_name = poke.get("pokemon").get("name")
            poke_encounters = []
            for version in poke.get("version_details"):
                poke_encounters.append(
                    {
                        "version": version.get("version").get("name"),
                        "encounter_details": version.get("encounter_details"),
                    }
                )

            self.encounters[poke_name] = poke_encounters

        self.encounter_methods = []
        for method in data.get("encounter_method_rates"):
            self.encounter_methods.append(method)

    def print_data(self):
        console.clear()
        return
