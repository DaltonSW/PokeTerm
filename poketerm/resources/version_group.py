from poketerm.utils.api import GetIDFromURL

from poketerm.resources.data import Resource


class VersionGroup(Resource):

    ENDPOINT = "version-group"

    def __init__(self, data):
        super().__init__(data)

        self.generationID = GetIDFromURL(data["generation"]["url"])
        self.versions = [thing["name"] for thing in data["versions"]]

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def print_data(self):
        pass

    def __str__(self):
        return ""
