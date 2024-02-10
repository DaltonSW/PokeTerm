from poketerm.utils.api import get_ID_from_URL

from poketerm.resources.data import Resource


class VersionGroup(Resource):

    ENDPOINT = "version-group"

    def __init__(self, data):
        super().__init__(data)

        self.generationID = get_ID_from_URL(data["generation"]["url"])
        self.versions = [thing["name"] for thing in data["versions"]]

    def print_data(self):
        pass

    def __str__(self):
        return ""
