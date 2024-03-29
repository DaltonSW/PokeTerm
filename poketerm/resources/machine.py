from poketerm.resources.data import Resource
from poketerm.console import console
from poketerm.utils.api import get_ID_from_URL


class Machine(Resource):
    MAX_COUNT = 1688
    ENDPOINT = "machine"
    VALID_NAMES = set()

    def __init__(self, data):
        super().__init__(data)

        item_data = data.get("item")
        if item_data:
            self.item_ID = get_ID_from_URL(item_data.get("url"))

        move_data = data.get("move")
        if move_data:
            self.move_ID = get_ID_from_URL(move_data.get("url"))

        version_group_data = data.get("version_group")
        if version_group_data:
            self.version_group_ID = get_ID_from_URL(version_group_data.get("url"))

    def print_data(self):
        console.clear()
        return
