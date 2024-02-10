from rich.table import Table
from rich import box
from rich.progress import (
    Progress,
    TextColumn,
    MofNCompleteColumn,
    BarColumn,
    TimeRemainingColumn,
)
from poketerm.console import console
from poketerm.resources.data import Resource
from poketerm.resources import move
from poketerm.utils.searching import SearchManager

from poketerm.config import Config

TYPE_ARRAY = [
    "normal",
    "fire",
    "water",
    "electric",
    "grass",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy",
]


class Type(Resource):
    MAX_COUNT = 18
    ENDPOINT = "type"
    VALID_NAMES = set()

    def __init__(self, data):
        super().__init__(data)

        damageRelationData = data.get("damage_relations")
        (
            self.noDamageTo,
            self.halfDamageTo,
            self.doubleDamageTo,
            self.noDamageFrom,
            self.halfDamageFrom,
            self.doubleDamageFrom,
        ) = self.ExtractDamageRelations(damageRelationData)

        pokemonData = data.get("pokemon")
        self.primaryPokes, self.secondaryPokes = self.ExtractPokemonRelations(
            pokemonData
        )

        self.moves = [thing.get("name") for thing in data.get("moves")]

    @staticmethod
    def ExtractDamageRelations(damageRelationData):
        noDamageTo = [
            thing.get("name") for thing in damageRelationData.get("no_damage_to")
        ]
        halfDamageTo = [
            thing.get("name") for thing in damageRelationData.get("half_damage_to")
        ]
        doubleDamageTo = [
            thing.get("name") for thing in damageRelationData.get("double_damage_to")
        ]
        noDamageFrom = [
            thing.get("name") for thing in damageRelationData.get("no_damage_from")
        ]
        halfDamageFrom = [
            thing.get("name") for thing in damageRelationData.get("half_damage_from")
        ]
        doubleDamageFrom = [
            thing.get("name") for thing in damageRelationData.get("double_damage_from")
        ]
        return (
            noDamageTo,
            halfDamageTo,
            doubleDamageTo,
            noDamageFrom,
            halfDamageFrom,
            doubleDamageFrom,
        )

    @staticmethod
    def ExtractPokemonRelations(pokemonRelationData):
        primaryPokes = []
        secondaryPokes = []

        for poke in pokemonRelationData:
            pokeName = poke.get("pokemon").get("name")
            # pokeObj = Pokemon.Pokemon.HandleSearch(pokeName)

            if poke.get("slot") == 1:
                primaryPokes.append(pokeName.title())

            elif poke.get("slot") == 2:
                secondaryPokes.append(pokeName.title())

        return primaryPokes, secondaryPokes

    def __str__(self):
        return ""

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
    def print_name(self) -> str:
        return f"[{self.name}]{self.name.title()}[/]"

    def print_data(self):
        console.print(f"[bold]Type: {self.print_name}[/]")
        print()

        self.PrintTypeEfficacyTable()
        self.PrintPossibilities()

    def PrintTypeEfficacyTable(self):
        print()
        if not Config.TYPE_FLAGS["efficacy"]:
            console.rule("Type [E]ffectiveness ▶", align="left", characters=" ")
            return

        console.rule("Type [E]ffectiveness ▼", align="left", characters=" ")
        defTable = Type.GetTypeTable("Defensive Information")
        defTable = self.SetTableData(defTable, self.GetDefensiveEffectiveness)
        console.print(defTable)

        offTable = Type.GetTypeTable("Offensive Information")
        offTable = self.SetTableData(offTable, self.GetOffensiveEffectiveness)
        console.print(offTable)
        console.rule(
            "Press any bracketed letter to expand/collapse the section.", characters=" "
        )

    def SetTableData(self, table, effectivenessFunction):
        typeEffs = [1 for _ in range(18)]
        for index, otherType in enumerate(TYPE_ARRAY):
            typeEffs[index] *= effectivenessFunction(otherType)
        str_effs = self.SetTypeEffectiveness(typeEffs)
        table.add_row(*str_effs)
        return table

    @staticmethod
    def SetTypeEffectiveness(typeEffs):
        strEffs = []
        for t in typeEffs:
            match t:
                case 0.5:
                    out = "[red]1/2"
                case 0.25:
                    out = "[red]1/4"
                case 2:
                    out = "[green]2"
                case 0:
                    out = "[red]0"
                case _:
                    out = "[gray]1"
            strEffs.append(out)

        return strEffs

    def PrintPossibilities(self):
        infoTable = Table(box=box.SIMPLE, show_header=False)

        infoTable.add_column("Primary")
        infoTable.add_column("Secondary")
        infoTable.add_column("Moves")

        primaryPokes = self.GetPrimaryPokesTable()
        secondaryPokes = self.GetSecondaryPokesTable()
        moveTable = self.GetAvailableMovesTable()

        if primaryPokes is None:
            primary = f"[P]rimary Typing ({len(self.primaryPokes)}) ▶"
        else:
            primary = primaryPokes

        if secondaryPokes is None:
            secondary = f"[S]econdary Typing ({len(self.secondaryPokes)}) ▶"
        else:
            secondary = secondaryPokes

        if moveTable is None:
            moveTable = f"[M]oves Available ({len(self.moves)}) ▶"

        infoTable.add_row(primary, secondary, moveTable)

        console.print(infoTable)

    def GetPrimaryPokesTable(self) -> Table | None:
        if not Config.TYPE_FLAGS["primary"]:
            return None

        else:
            pokeTable = Table(title=f"[P]rimary Typing ({len(self.primaryPokes)}) ▼")
            pokeTable.add_column("Pokemon")
            # pokeTable.add_column("Type 1")
            # pokeTable.add_column("Type 2")

            for pokeInfo in self.primaryPokes:
                pokeTable.add_row(pokeInfo)

        return pokeTable

    def GetSecondaryPokesTable(self) -> Table | None:
        if not Config.TYPE_FLAGS["secondary"]:
            return None

        else:
            pokeTable = Table(
                title=f"[S]econdary Typing ({len(self.secondaryPokes)}) ▼"
            )
            pokeTable.add_column("Pokemon")
            # pokeTable.add_column("Type 1")
            # pokeTable.add_column("Type 2")

            for pokeInfo in self.secondaryPokes:
                pokeTable.add_row(pokeInfo)

        return pokeTable

    def GetAvailableMovesTable(self) -> Table | None:
        if not Config.TYPE_FLAGS["moves"]:
            return None

        newTable = Table(title=f"[M]oves Available ({len(self.moves)}) ▼")
        newTable.add_column("Move")
        newTable.add_column("Power")
        newTable.add_column("Acc.")
        newTable.add_column("PP")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            transient=True,
        ) as progress:
            moveQuery = progress.add_task("Querying moves...", total=len(self.moves))
            for moveName in self.moves:
                moveObj = SearchManager.handle_search_and_cast(move.Move, moveName)
                if moveObj:
                    newTable.add_row(
                        moveObj.print_name,
                        str(moveObj.power),
                        str(moveObj.accuracy),
                        str(moveObj.PP),
                    )
                progress.update(moveQuery, advance=1)

        return newTable

    @classmethod
    def toggle_flag(cls, flag: str):
        match flag:
            case "e":
                Config.TYPE_FLAGS["efficacy"] = not Config.TYPE_FLAGS["efficacy"]
            case "p":
                Config.TYPE_FLAGS["primary"] = not Config.TYPE_FLAGS["primary"]
            case "s":
                Config.TYPE_FLAGS["secondary"] = not Config.TYPE_FLAGS["secondary"]
            case "m":
                Config.TYPE_FLAGS["moves"] = not Config.TYPE_FLAGS["moves"]
            case _:
                return

    @staticmethod
    def GetTypeTable(title: str) -> Table:
        typeTable = Table(
            title=title, box=box.ROUNDED, title_justify="left", show_lines=True
        )

        typeTable.add_column("NOR", header_style="normal", justify="center")
        typeTable.add_column("FIR", header_style="fire", justify="center")
        typeTable.add_column("WAT", header_style="water", justify="center")
        typeTable.add_column("ELE", header_style="electric", justify="center")
        typeTable.add_column("GRA", header_style="grass", justify="center")
        typeTable.add_column("ICE", header_style="ice", justify="center")
        typeTable.add_column("FIG", header_style="fighting", justify="center")
        typeTable.add_column("POI", header_style="poison", justify="center")
        typeTable.add_column("GRO", header_style="ground", justify="center")
        typeTable.add_column("FLY", header_style="flying", justify="center")
        typeTable.add_column("PSY", header_style="psychic", justify="center")
        typeTable.add_column("BUG", header_style="bug", justify="center")
        typeTable.add_column("ROC", header_style="rock", justify="center")
        typeTable.add_column("GHO", header_style="ghost", justify="center")
        typeTable.add_column("DRA", header_style="dragon", justify="center")
        typeTable.add_column("DAR", header_style="dark", justify="center")
        typeTable.add_column("STE", header_style="steel", justify="center")
        typeTable.add_column("FAI", header_style="fairy", justify="center")

        return typeTable
