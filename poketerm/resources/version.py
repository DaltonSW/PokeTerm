from poketerm.utils.api import get_ID_from_URL

from poketerm.resources.data import Resource


class Version(Resource):

    ENDPOINT = "version"

    def __init__(self, data):
        super().__init__(data)

        self.versionGroupID = get_ID_from_URL(data["version_group"]["url"])

    def print_data(self):
        print(self.print_name)
        print(f"Version Group ID: {self.versionGroupID}")
        pass

    def __str__(self):
        return ""
