import Utils
from rich.table import Table
from rich import box
from console import console
from Resources.Data import AbstractData

TYPE_ARRAY = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting',
              'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost',
              'dragon', 'dark', 'steel', 'fairy']

# TODO:
#   Pokemon w/ this as primary and secondary type, two tables next to each other

class Type(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'type'

    def __init__(self, data):
        super().__init__(data)

        damageRelations = data.get('damage_relations')
        self.noDamageTo = [thing.get('name') for thing in damageRelations.get('no_damage_to')]
        self.halfDamageTo = [thing.get('name') for thing in damageRelations.get('half_damage_to')]
        self.doubleDamageTo = [thing.get('name') for thing in damageRelations.get('double_damage_to')]
        self.noDamageFrom = [thing.get('name') for thing in damageRelations.get('no_damage_from')]
        self.halfDamageFrom = [thing.get('name') for thing in damageRelations.get('half_damage_from')]
        self.doubleDamageFrom = [thing.get('name') for thing in damageRelations.get('double_damage_from')]

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def __str__(self):
        return ''

    def GetOffensiveEffectiveness(self, otherType) -> float:
        if otherType in self.noDamageTo:
            return 0
        elif otherType in self.halfDamageTo:
            return 0.5
        elif otherType in self.doubleDamageTo:
            return 2
        else:
            return 1

    def GetDefensiveEffectiveness(self, otherType) -> float:
        if otherType in self.noDamageFrom:
            return 0
        elif otherType in self.halfDamageFrom:
            return 0.5
        elif otherType in self.doubleDamageFrom:
            return 2
        else:
            return 1

    @property
    def PrintName(self) -> str:
        return f'[{self.name}]{self.name.title()}[/]'

    def PrintData(self):
        console.print(f"[bold]Type: {self.PrintName}[/]")
        print()

        defTable = Type.GetTypeTable("Defensive Information")

        typeEffs = [1 for _ in range(18)]

        for index, otherType in enumerate(TYPE_ARRAY):
            typeEffs[index] *= self.GetDefensiveEffectiveness(otherType)

        strEffs = []
        for t in typeEffs:
            match t:
                case 0.5:
                    out = '[red]1/2'
                case 0.25:
                    out = '[red]1/4'
                case 2:
                    out = '[green]2'
                case _:
                    out = '[gray]1'
            strEffs.append(out)
        defTable.add_row(*strEffs)

        console.print(defTable)
        print()

        offTable = Type.GetTypeTable("Offensive Information")

        typeEffs = [1 for _ in range(18)]

        for index, otherType in enumerate(TYPE_ARRAY):
            typeEffs[index] *= self.GetOffensiveEffectiveness(otherType)

        strEffs = []
        for t in typeEffs:
            match t:
                case 0.5:
                    out = '[red]1/2'
                case 0.25:
                    out = '[red]1/4'
                case 2:
                    out = '[green]2'
                case _:
                    out = '[gray]1'
            strEffs.append(out)
        offTable.add_row(*strEffs)

        console.print(offTable)

    def AddToCache(self):
        super().AddToCache()

    @staticmethod
    def GetTypeTable(title: str) -> Table:
        typeTable = Table(title=title, box=box.ROUNDED, title_justify='left', show_lines=True)

        typeTable.add_column("NOR", header_style='normal', justify='center')
        typeTable.add_column("FIR", header_style='fire', justify='center')
        typeTable.add_column("WAT", header_style='water', justify='center')
        typeTable.add_column("ELE", header_style='electric', justify='center')
        typeTable.add_column("GRA", header_style='grass', justify='center')
        typeTable.add_column("ICE", header_style='ice', justify='center')
        typeTable.add_column("FIG", header_style='fighting', justify='center')
        typeTable.add_column("POI", header_style='poison', justify='center')
        typeTable.add_column("GRO", header_style='ground', justify='center')
        typeTable.add_column("FLY", header_style='flying', justify='center')
        typeTable.add_column("PSY", header_style='psychic', justify='center')
        typeTable.add_column("BUG", header_style='bug', justify='center')
        typeTable.add_column("ROC", header_style='rock', justify='center')
        typeTable.add_column("GHO", header_style='ghost', justify='center')
        typeTable.add_column("DRA", header_style='dragon', justify='center')
        typeTable.add_column("DAR", header_style='dark', justify='center')
        typeTable.add_column("STE", header_style='steel', justify='center')
        typeTable.add_column("FAI", header_style='fairy', justify='center')

        return typeTable
