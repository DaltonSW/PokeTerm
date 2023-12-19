import Colors
import Utils
from .Data import AbstractData
from tabulate import tabulate
from termcolor import colored

ID_TO_NAME_CACHE = {}
NAME_TO_DATA_CACHE = {}
ENDPOINT = 'move'


class Move(AbstractData):
    def __init__(self, data):
        super().__init__()
        global ID_TO_NAME_CACHE
        self.ID: int = data.get('id')
        self.name: str = data.get('name')
        self.accuracy: int = data.get('accuracy')
        self.effectChance: int = data.get('effect_chance')
        self.PP: int = data.get('pp')
        self.priority: int = data.get('priority')
        self.power: int = data.get('power')
        self.moveClass: str = data.get('damage_class').get('name')
        self.type: str = data.get('type').get('name')
        ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        Utils.ClearScreen()

        infoTable = [
            [colored("Move:", attrs=["bold"]), f' {self.PrintName} [{self.ID}]'],
            [colored("Type: ", attrs=["bold"]), f' {self.FormattedMoveType}'],
            [colored("Class: ", attrs=["bold"]), f' {self.FormattedMoveClass}']
        ]
        print(tabulate(infoTable, tablefmt='plain'))
        statHeaders = ["PP", "Power", "Accuracy", ]
        statCells = [[self.PP, self.power, f'{self.accuracy}%']]
        print(tabulate(statCells, headers=statHeaders))
        return

    # region Formatted Getters
    @property
    def FormattedMoveClass(self) -> str:
        return colored(self.moveClass.title(), Colors.GetMoveClassColor(self.moveClass))

    @property
    def FormattedMoveType(self) -> str:
        return colored(self.type.title(), Colors.GetTypeColor(self.type))

    # endregion


def LoadCache():
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    data = Utils.LoadCache(ENDPOINT)
    try:
        ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE = data
    except TypeError:
        print(f"Failed to load {ENDPOINT.upper()} cache")
        pass


def SaveCache():
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    if len(NAME_TO_DATA_CACHE) == 0:
        return
    output = (ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE)
    Utils.SaveCache(ENDPOINT, output)


def HandleSearch() -> Move | None:
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    query = input(f'{ENDPOINT.title()} Name or ID: ').lower()

    if query.isdigit():
        query = Utils.ProperQueryFromID(int(query), ID_TO_NAME_CACHE)

    if query in NAME_TO_DATA_CACHE:
        return NAME_TO_DATA_CACHE[query]

    data = Utils.GetFromAPIWrapper(ENDPOINT, query)
    if data is not None:
        newObject = Move(data)
        NAME_TO_DATA_CACHE[newObject.name] = newObject
        return newObject
