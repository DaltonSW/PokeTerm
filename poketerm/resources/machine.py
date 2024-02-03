from poketerm.resources.data import AbstractData
from poketerm.console import console
from poketerm.utils.api import GetIDFromURL


class Machine(AbstractData):
    MAX_COUNT = 1688
    ENDPOINT = "machine"
    VALID_NAMES = set()
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}

    def __init__(self, data):
        super().__init__(data)

        item_data = data.get("item")
        if item_data:
            self.item_ID = GetIDFromURL(item_data.get("url"))

        move_data = data.get("move")
        if move_data:
            self.move_ID = GetIDFromURL(move_data.get("url"))

        version_group_data = data.get("version_group")
        if version_group_data:
            self.version_group_ID = GetIDFromURL(version_group_data.get("url"))

    def PrintData(self):
        console.clear()
        return

    def AddToCache(self):
        super().AddToCache()
