import Utils
from .Data import AbstractData
from tabulate import tabulate
from termcolor import colored

ID_TO_NAME_CACHE = {}
NAME_TO_DATA_CACHE = {}
ENDPOINT = 'move'


class Move(AbstractData):
    """
    This is the documentation for the Move class.

    Attributes:
        ID (int): The ID of the move.
        name (str): The name of the move.
        accuracy (int): The accuracy of the move.
        effectChance (int): The chance of the move having an effect.
        PP (int): The number of Power Points (PP) of the move.
        priority (int): The priority of the move.
        power (int): The power of the move.
        moveClass (str): The class of the move.
        type (str): The type of the move.

    Methods:
        PrintData(self) -> None: Prints the move information.

    Example usage:
        move = Move(data)
        move.PrintData()
    """
    def __init__(self, data):
        global ID_TO_NAME_CACHE
        self.ID: int = data.get('id')
        self.name: str = data.get('name')
        self.accuracy = data.get('accuracy')
        self.effectChance = data.get('effect_chance')
        self.PP = data.get('pp')
        self.priority = data.get('priority')
        self.power = data.get('power')
        self.moveClass = data.get('damage_class').get('name')
        self.type = data.get('type').get('name')
        ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        # print(f'Move Information:\n'
        #       f' {move.name.title()} [{move.ID}]\n'
        #       f' - Accuracy: {move.accuracy}\n'
        #       f' - Effect Chance: {move.effectChance}\n'
        #       f' - PP: {move.PP}\n'
        #       f' - Priority: {move.priority}\n'
        #       f' - Power: {move.power}\n'
        #       f' - Class: {move.moveClass.title()}\n'
        #       f' - Type: {move.type.title()}\n')

        Utils.ClearScreen()

        infoTable = [
            [colored("Move:", attrs=["bold"]), f' {self.name.title()} [{self.ID}]'],
            [colored("Type: ", attrs=["bold"]), f' {self.type.title()}'],
            [colored("Class: ", attrs=["bold"]), f' {self.moveClass.title()}']
        ]
        print(tabulate(infoTable, tablefmt='plain'))
        statHeaders = ["PP", "Power", "Accuracy", ]
        statCells = [[self.PP, self.power, self.accuracy]]
        print(tabulate(statCells, headers=statHeaders))
        return


def LoadCache():
    """
    LoadCache()

    Loads the cache data from the specified endpoint and updates the global cache variables.

    :return: None
    """
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    data = Utils.LoadCache(ENDPOINT)
    try:
        ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE = data
    except TypeError:
        print(f"Failed to load {ENDPOINT.upper()} cache")
        pass


def SaveCache():
    """
    Saves the ID_TO_NAME_CACHE and NAME_TO_DATA_CACHE to a file using the Utils.SaveCache method.

    :return: None
    """
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    if len(NAME_TO_DATA_CACHE) == 0:
        return
    output = (ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE)
    Utils.SaveCache(ENDPOINT, output)


def HandleSearch() -> Move | None:
    """

    HandleSearch

    """
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    query = input(f'{ENDPOINT.title()} Name or ID: ').lower()

    if query.isdigit():
        query = Utils.ProperQueryFromID(query, ID_TO_NAME_CACHE)

    if query in NAME_TO_DATA_CACHE:
        return NAME_TO_DATA_CACHE[query]

    data = Utils.GetFromAPIWrapper(ENDPOINT, query)
    if data is not None:
        newObject = Move(data)
        NAME_TO_DATA_CACHE[newObject.name] = newObject
        return newObject

