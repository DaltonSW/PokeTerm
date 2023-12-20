import Utils
from Resources.Data import AbstractData


class Version(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'version-group'

    def __init__(self, data):
        super().__init__(data)

        self.generationID = Utils.GetIDFromURL(data['generation']['url'])

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        pass

    def __str__(self):
        return ''

    def AddToCache(self):
        super().AddToCache()
