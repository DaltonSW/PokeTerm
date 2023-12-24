import Utils
from .Data import AbstractData
from console import console

# TODO:
#   List Pokemon that can learn this move
#   List TM number in each gen, if applicable

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
            [f"[bold]Move:[/] {self.PrintName} [{self.ID}]"],
            [f"[bold]Type:[/] {self.FormattedMoveType}"],
            [f"[bold]Class:[/] {self.FormattedMoveClass}"]
        ]
        console.print(tabulate(infoTable, tablefmt='plain'))
        statHeaders = ["PP", "Power", "Accuracy", ]
        statCells = [[self.PP, self.power, f'{self.accuracy}%']]
        console.print(tabulate(statCells, headers=statHeaders))
        return

    def AddToCache(self):
        super().AddToCache()

    # region Formatted Getters
    @property
    def FormattedMoveClass(self) -> str:
        return f'[{self.moveClass}]{self.moveClass.title()}[/]'

    @property
    def FormattedMoveType(self) -> str:
        return f'[{self.type}]{self.type.title()}[/]'

    # endregion

