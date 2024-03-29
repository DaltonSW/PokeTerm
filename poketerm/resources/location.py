from poketerm.resources.data import Resource
from poketerm.console import console


class Location(Resource):
    MAX_COUNT = 867
    ENDPOINT = "location"
    VALID_NAMES = set()

    def __init__(self, data):
        super().__init__(data)

        self.areas = []
        for area in data.get("areas"):
            self.areas.append(area.get("name"))

        self.region = data.get("region").get("name")

    def print_data(self):
        console.clear()
        return
