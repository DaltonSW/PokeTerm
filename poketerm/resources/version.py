from poketerm.utils.api import GetIDFromURL

from poketerm.resources.data import Resource


class Version(Resource):

    ENDPOINT = "version"

    def __init__(self, data):
        super().__init__(data)

        self.versionGroupID = GetIDFromURL(data["version_group"]["url"])

    def print_data(self):
        print(self.PrintName)
        print(f"Version Group ID: {self.versionGroupID}")
        pass

    def __str__(self):
        return ""
