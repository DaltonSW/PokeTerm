from poketerm.resources.data import Resource

# TODO:
#   List out each ability
#   List out each move
#   List out each Species added


class Generation(Resource):
    MAX_COUNT = 9
    ENDPOINT = "generation"
    VALID_NAMES = set()

    def __init__(self, data):
        super().__init__(data)

        self.abilitiesIntroduced: list[str] = [
            thing["name"] for thing in data["abilities"]
        ]
        self.movesIntroduced: list[str] = [thing["name"] for thing in data["moves"]]
        self.speciesIntroduced: list[str] = [
            thing["name"] for thing in data["pokemon_species"]
        ]

        self.versionGroups: list[str] = [
            thing["name"] for thing in data["version_groups"]
        ]

    def print_data(self):
        print(f"Generation {self.ID}")
        print(f"Abilities Introduced: {len(self.abilitiesIntroduced)}")
        print(f"Moves Introduced: {len(self.movesIntroduced)}")
        print(f"Species Introduced: {len(self.speciesIntroduced)}")

    def __str__(self):
        return ""
