from rich.table import Table
import re

from poketerm.resources.data import AbstractData
from poketerm.console import console

# TODO:
#   List Pokemon that can learn this move
#   List TM number in each gen, if applicable


class Move(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = "move"

    def __init__(self, data):
        super().__init__(data)

        self.accuracy: int = data.get("accuracy")
        self.effectChance: int = data.get("effect_chance")
        self.PP: int = data.get("pp")
        self.priority: int = data.get("priority")
        self.power: int = data.get("power")
        self.moveClass: str = data.get("damage_class").get("name")
        self.type: str = data.get("type").get("name")
        self.effectEntry: str = data.get("effect_entries")[0].get("effect")

    def PrintData(self):
        console.clear()

        console.print(f"[bold]Move:[/] {self.PrintName} [[bold]{self.ID}[/]]")
        console.print(f"[bold]Type:[/] {self.FormattedMoveType}")
        console.print(f"[bold]Class:[/] {self.FormattedMoveClass}")
        console.print(f"[bold]Description:[/] {self.FormattedEffectEntry}")

        statTable = Table()
        statTable.add_column("PP")
        statTable.add_column("Power")
        statTable.add_column("Accuracy")
        statTable.add_row(str(self.PP), str(self.power), f"{self.accuracy}%")
        console.print(statTable)
        return

    def AddToCache(self):
        super().AddToCache()

    # region Formatted Getters
    @property
    def FormattedMoveClass(self) -> str:
        return f"[{self.moveClass}]{self.moveClass.title()}[/]"

    @property
    def FormattedMoveType(self) -> str:
        return f"[{self.type}]{self.type.title()}[/]"
    
    @property
    def FormattedEffectEntry(self) -> str:
        return f"{re.sub("\$effect_chance%", str(self.effectChance) + "%", self.effectEntry)}"

    # endregion
