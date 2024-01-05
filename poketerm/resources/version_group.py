from poketerm import utils
from poketerm.resources.data import AbstractData


class VersionGroup(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = "version-group"

    def __init__(self, data):
        super().__init__(data)

        self.generationID = utils.GetIDFromURL(data["generation"]["url"])
        self.versions = [thing["name"] for thing in data["versions"]]

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        pass

    def __str__(self):
        return ""

    def AddToCache(self):
        super().AddToCache()
