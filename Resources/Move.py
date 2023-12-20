import Colors
import Utils
from .Data import AbstractData
from tabulate import tabulate
from termcolor import colored

# TODO: Descriptions and stuff
class Move(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'move'

    def __init__(self, data):
        super().__init__(data)

        self.accuracy: int = data.get('accuracy')
        self.effectChance: int = data.get('effect_chance')
        self.PP: int = data.get('pp')
        self.priority: int = data.get('priority')
        self.power: int = data.get('power')
        self.moveClass: str = data.get('damage_class').get('name')
        self.type: str = data.get('type').get('name')

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

    def AddToCache(self):
        super().AddToCache()

    # region Formatted Getters
    @property
    def FormattedMoveClass(self) -> str:
        return colored(self.moveClass.title(), Colors.GetMoveClassColor(self.moveClass))

    @property
    def FormattedMoveType(self) -> str:
        return colored(self.type.title(), Colors.GetTypeColor(self.type))

    # endregion

