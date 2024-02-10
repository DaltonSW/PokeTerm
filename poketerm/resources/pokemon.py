from bs4 import BeautifulSoup
import requests
from poketerm.utils.constants import VERSION_MAPPING_DICT, REVERSED_MAPPING_DICT
from poketerm.resources.data import Resource
from poketerm.resources import species, ability, version_group, type
from poketerm.resources import generation
from poketerm.utils.searching import SearchManager
from poketerm.config import Config

from rich.table import Table
from rich import box
from poketerm.console import console

# TODO:
#   Override the search so if it fails to find a pokemon by the name, it searches for a species, then shows the default form
#   Dex information


class Pokemon(Resource):
    MAX_COUNT = 1025
    ENDPOINT = "pokemon"
    VALID_NAMES = set()

    def __init__(self, data):
        super().__init__(data)

        # region Abilities
        self.possibleAbilities = []
        self.hiddenAbility = None
        abilityList: list = data.get("abilities")
        for abil in abilityList:
            newAbility = SearchManager.handle_search_and_cast(
                ability.Ability, abil.get("ability").get("name")
            )
            if newAbility is not None:
                if abil.get("is_hidden") is True:
                    self.hiddenAbility = newAbility
                else:
                    self.possibleAbilities.append(newAbility)
        # endregion

        # Species
        spec = SearchManager.handle_search_and_cast(
            species.Species, data.get("species").get("name")
        )
        if spec is not None:
            self.speciesID = spec.ID

        # Stats
        self.baseStats = {}
        self.EVs = {}
        for stat in data.get("stats"):
            statName = stat.get("stat").get("name")
            self.baseStats[statName] = int(stat.get("base_stat"))
            self.EVs[statName] = int(stat.get("effort"))

        # Available Locations
        self.locationInformation = self.LocationLoader()

        self.shinyLink = (
            data.get("sprites").get("other").get("official-artwork").get("front_shiny")
        )

        # TODO:
        #   First Generation Appearance (Species)
        #   National Dex Number (Species)

        # TODO:
        #   List of moves (probably just in Gen 9 for right now)
        #   Other forms

        typeData = data.get("types")

        self.typeArray = []

        self.typeArray.append(typeData[0].get("type").get("name"))
        if len(typeData) > 1:
            self.typeArray.append(typeData[1].get("type").get("name"))

    def print_data(self):
        console.rule(f"[bold]{self.name.upper()}[/]", style="none")
        console.print(f"[link={self.shinyLink}]Shiny Link (ctrl + click)[/]")

        self.PrintTypeInfo()
        self.PrintSpeciesInfo()
        self.PrintAbilityInfo()
        self.PrintStatInfo()
        self.PrintVersionInfo()
        console.rule(
            "Press any bracketed letter to expand/collapse the section.", characters=" "
        )
        return

    def PrintSpeciesInfo(self):
        print()
        if not Config.POKEMON_FLAGS["species"]:
            console.rule("Spe\[c]ies Information ▶", align="left", characters=" ")
            return

        console.rule("Spe\[c]ies Information ▼", align="left", characters=" ")
        spec = SearchManager.handle_search_and_cast(species.Species, self.speciesID)
        if spec is not None:
            spec.PrintDataForPokemonPage()
            spec.print_data()
        return

    def PrintTypeInfo(self) -> None:
        print()
        if not Config.POKEMON_FLAGS["typing"]:
            console.rule("[T]ype Information ▶", align="left", characters=" ")
            return

        console.rule("[T]ype Information ▼", align="left", characters=" ")
        print()
        console.print(f"Typing: {self.FormattedTypeOne}{self.FormattedTypeTwo}")

        typeTable = type.Type.GetTypeTable("Type Defenses")

        typeEffs = [1 for _ in range(18)]

        for index, otherType in enumerate(type.TYPE_ARRAY):
            typeOneObj = SearchManager.handle_search_and_cast(
                type.Type, self.typeArray[0]
            )
            typeEffs[index] *= typeOneObj.GetDefensiveEffectiveness(otherType)
            if len(self.typeArray) > 1:
                typeTwoObj = SearchManager.handle_search_and_cast(
                    type.Type, self.typeArray[1]
                )
                typeEffs[index] *= typeTwoObj.GetDefensiveEffectiveness(otherType)

        strEffs = []
        for t in typeEffs:
            match t:
                case 0.5:
                    out = "[red]1/2"
                case 0.25:
                    out = "[red]1/4"
                case 2:
                    out = "[green]2"
                case _:
                    out = "[gray]1"
            strEffs.append(out)
        typeTable.add_row(*strEffs)

        console.print(typeTable)

    def PrintAbilityInfo(self) -> None:
        print()
        if not Config.POKEMON_FLAGS["abilities"]:
            console.rule("[P]ossible Abilities ▶", align="left", characters=" ")
            return

        console.rule("[P]ossible Abilities ▼", align="left", characters=" ")

        abilityTable = Table(box=box.ROUNDED, show_lines=True)

        abilityTable.add_column("Ability")
        abilityTable.add_column("Description")

        for possibleAbility in self.possibleAbilities:
            abilityTable.add_row(
                f"[bold]{possibleAbility.name.title()}[/]",
                possibleAbility.print_description,
            )
        if self.hiddenAbility is not None:
            abilityTable.add_row(
                f"[bold]{self.hiddenAbility.name.title()} (H)[/]",
                self.hiddenAbility.print_description,
            )
        console.print(abilityTable)

    def PrintStatInfo(self) -> None:
        print()
        if not Config.POKEMON_FLAGS["stats"]:
            console.rule("[S]tat Information ▶", align="left", characters=" ")
            return

        console.rule("[S]tat Information ▼", align="left", characters=" ")

        statsTable = Table(box=box.ROUNDED)

        # I don't care about the hardcoding, this is way more readable
        statsTable.add_column("HP", header_style="hp")
        statsTable.add_column("Attack", header_style="attack")
        statsTable.add_column("Defense", header_style="defense")
        statsTable.add_column("Sp Atk", header_style="special-attack")
        statsTable.add_column("Sp Def", header_style="special-defense")
        statsTable.add_column("Speed", header_style="speed")
        statsTable.add_column("Total")

        statsTable.add_row(
            str(self.baseStats["hp"]),
            str(self.baseStats["attack"]),
            str(self.baseStats["defense"]),
            str(self.baseStats["special-attack"]),
            str(self.baseStats["special-defense"]),
            str(self.baseStats["speed"]),
            str(sum(self.baseStats.values())),
        )

        console.print(statsTable)

        outputStr = "[bold]EV Yield:[/] "
        if self.EVs["hp"] != 0:
            outputStr += f"[hp]{str(self.EVs['hp'])} HP[/hp], "
        if self.EVs["attack"] != 0:
            outputStr += f"[attack]{str(self.EVs['attack'])} Attack[/attack], "
        if self.EVs["defense"] != 0:
            outputStr += f"[defense]{str(self.EVs['defense'])} Defense[/defense], "
        if self.EVs["special-attack"] != 0:
            outputStr += f"[special-attack]{str(self.EVs['special-attack'])} Sp. Attack[/special-attack], "
        if self.EVs["special-defense"] != 0:
            outputStr += f"[special-defense]{str(self.EVs['special-defense'])} Sp. Defense[/special-defense], "
        if self.EVs["speed"] != 0:
            outputStr += f"[speed]{str(self.EVs['speed'])} Speed[/speed], "

        console.print(outputStr[:-2])

    def PrintVersionInfo(self) -> None:
        print()
        if not Config.POKEMON_FLAGS["availability"]:
            print("[A]vailability Info ▶")
            return

        available, unavailable = [], []
        if self.locationInformation is None:
            return
        for game in self.locationInformation.keys():
            locations = self.locationInformation[game]
            if len(locations) == 0:
                unavailable.append(game)
            else:
                available.append(game)

        overallInfoTable = Table(
            title="[A]vailability Info ▼",
            title_justify="left",
            box=box.HORIZONTALS,
            show_header=False,
            show_lines=True,
        )

        overallInfoTable.add_column()
        overallInfoTable.add_column()
        overallInfoTable.add_column()

        with console.status("Querying for location data..."):
            overallInfoTable.add_row(
                self.GetGenerationTable(1),
                self.GetGenerationTable(2),
                self.GetGenerationTable(3),
            )
            overallInfoTable.add_row(
                self.GetGenerationTable(4),
                self.GetGenerationTable(5),
                self.GetGenerationTable(6),
            )
            overallInfoTable.add_row(
                self.GetGenerationTable(7),
                self.GetGenerationTable(8),
                self.GetGenerationTable(9),
            )

        # TODO: Eventually implement an "ignore certain generations" flag

        console.print(overallInfoTable)

    def GetGenerationTable(self, gen):
        genTable = Table(title=f"Generation {gen}")
        genTable.add_column("Game")
        genTable.add_column("Location")
        genInfo = SearchManager.handle_search_and_cast(generation.Generation, gen)
        for versionGroup in genInfo.versionGroups:
            groupInfo = SearchManager.handle_search_and_cast(
                version_group.VersionGroup, versionGroup
            )
            for version in groupInfo.versions:
                versionLocations = self.locationInformation.get(version)
                if versionLocations is None or len(versionLocations) == 0:
                    continue
                secondCell = ", ".join(versionLocations)
                genTable.add_row(
                    f"[{version}]{REVERSED_MAPPING_DICT[version]}[/]", secondCell
                )
        return genTable

    def LocationLoader(
        self,
    ) -> dict[str, list[str]] | None:  # eventually dict[int, list[int]] for IDs instead
        queryURL = f"https://pokemondb.net/pokedex/{self.name}"
        response = requests.get(queryURL)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the table with location information
        locationsDiv = soup.find("div", {"id": "dex-locations"})

        locationsTable = ""

        # Find the first table after the 'dex-locations' div
        if locationsDiv:
            locationsTable = locationsDiv.find_next("table")

        # Assuming 'location_table' is the BeautifulSoup object for the table
        locationRows = locationsTable.find_all("tr")

        encounters = {}
        for row in locationRows:
            games = []
            locations = []
            gamesHTML = row.find_next("th")
            for game in gamesHTML.find_all("span"):
                games.append(game.text)
            locationsHTML = row.find_next("td")
            for location in locationsHTML.find_all("a"):
                locations.append(location.text)

            for gameName in games:
                encounters[VERSION_MAPPING_DICT[gameName]] = locations
        # time.sleep(0.1)
        return encounters

    # endregion

    @property
    def FormattedTypeOne(self) -> str:
        typeOneObj = SearchManager.handle_search_and_cast(type.Type, self.typeArray[0])
        if typeOneObj is not None:
            return typeOneObj.print_name

    @property
    def FormattedTypeTwo(self) -> str:
        if len(self.typeArray) == 1:
            return ""
        typeTwoObj = SearchManager.handle_search_and_cast(type.Type, self.typeArray[1])
        if typeTwoObj is not None:
            return " [white]/[/] " + typeTwoObj.print_name

    @classmethod
    def toggle_flag(cls, flag: str):
        match flag:
            case "p":
                Config.POKEMON_FLAGS["abilities"] = not Config.POKEMON_FLAGS[
                    "abilities"
                ]
            case "s":
                Config.POKEMON_FLAGS["stats"] = not Config.POKEMON_FLAGS["stats"]
            case "a":
                Config.POKEMON_FLAGS["availability"] = not Config.POKEMON_FLAGS[
                    "availability"
                ]
            case "u":
                Config.POKEMON_FLAGS["unavailable"] = not Config.POKEMON_FLAGS[
                    "unavailable"
                ]
            case "t":
                Config.POKEMON_FLAGS["typing"] = not Config.POKEMON_FLAGS["typing"]
            case "c":
                Config.POKEMON_FLAGS["species"] = not Config.POKEMON_FLAGS["species"]
            case _:
                return
