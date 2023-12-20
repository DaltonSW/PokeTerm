import Colors
import Utils
from .Data import AbstractData
from tabulate import tabulate
from termcolor import colored


class Resource(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'resource'

    def __init__(self, data):
        super().__init__(data)

    def PrintData(self):
        Utils.ClearScreen()

        infoTable = [
            [colored(f"{self.ENDPOINT.title()}:", attrs=["bold"]), f' {self.PrintName} [{self.ID}]'],
        ]
        print(tabulate(infoTable, tablefmt='plain'))
        return

    def __str__(self):
        return ''

    def AddToCache(self):
        super().AddToCache()

    # region Formatted Getters
    # @property
    # def FormattedResourceProperty(self) -> str:
    #     return colored(self.property.title(), Colors.GetWhateverColor(self.property))

    # endregion
