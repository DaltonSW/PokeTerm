import Colors
import Utils
from .Data import AbstractData
from tabulate import tabulate
from termcolor import colored

ID_TO_NAME_CACHE = {}
NAME_TO_DATA_CACHE = {}
ENDPOINT = 'resource'

class Resource(AbstractData):
    def __init__(self, data):
        super().__init__()
        global ID_TO_NAME_CACHE
        self.ID: int = data.get('id')
        self.name: str = data.get('name')

        ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        Utils.ClearScreen()

        infoTable = [
            [colored(f"{ENDPOINT.title()}:", attrs=["bold"]), f' {self.PrintName} [{self.ID}]'],
        ]
        print(tabulate(infoTable, tablefmt='plain'))
        return

    # region Formatted Getters
    # @property
    # def FormattedResourceProperty(self) -> str:
    #     return colored(self.property.title(), Colors.GetWhateverColor(self.property))

    # endregion

def CheckCaches(query: int | str) -> Resource | None:
    if query.isdigit():
        if int(query) not in ID_TO_NAME_CACHE:
            return None
        name = ID_TO_NAME_CACHE[int(query)]
    else:
        name = query
    if query not in NAME_TO_DATA_CACHE:
        return None
    else:
        return NAME_TO_DATA_CACHE[name]

def AddToCache(resource: Resource):
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    ID_TO_NAME_CACHE[resource.ID] = resource.name
    NAME_TO_DATA_CACHE[resource.name] = resource

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


def HandleSearch() -> Resource | None:
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    query = input(f'{ENDPOINT.title()} Name or ID: ').lower()

    if query.isdigit():
        query = Utils.ProperQueryFromID(int(query), ID_TO_NAME_CACHE)

    if query in NAME_TO_DATA_CACHE:
        return NAME_TO_DATA_CACHE[query]

    data = Utils.GetFromAPIWrapper(ENDPOINT, query)
    if data is not None:
        newObject = Resource(data)
        NAME_TO_DATA_CACHE[newObject.name] = newObject
        return newObject
