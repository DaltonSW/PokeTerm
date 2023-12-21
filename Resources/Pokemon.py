from bs4 import BeautifulSoup
import requests
import Colors
import Utils
from Resources.Data import AbstractData
from tabulate import tabulate
from termcolor import colored, cprint
from Resources import Species, Ability, Generation, VersionGroup

from rich.table import Table
from rich import box
from console import console


class Pokemon(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    FLAGS = {
        'abilities'   : 1,
        'stats'       : 1,
        'availability': 1,
        'unavailable' : 1
    }
    ENDPOINT = 'pokemon'

    def __init__(self, data):
        super().__init__(data)

        # region Abilities
        self.possibleAbilities = []
        self.hiddenAbility = None
        abilityList: list = data.get('abilities')
        for ability in abilityList:
            newAbility = Ability.Ability.HandleSearch(ability.get('ability').get('name'))
            if newAbility is not None:
                if ability.get('get_hidden') is True:
                    self.hiddenAbility = newAbility
                else:
                    self.possibleAbilities.append(newAbility)
        # endregion

        # Species
        species = Species.Species.HandleSearch((data.get('species').get('name')))
        if species is not None:
            self.speciesID = species.ID

        # Stats
        self.baseStats = {}
        self.EVs = {}
        for stat in data.get('stats'):
            statName = stat.get('stat').get('name')
            self.baseStats[statName] = int(stat.get('base_stat'))
            self.EVs[statName] = int(stat.get('effort'))

        # Available Locations
        self.locationInformation = self.LocationLoader()

        # TODO: Set up type information and classes
        self.types = [t.get('type').get('name') for t in data.get('types')]

        # TODO: Pull other forms

        # TODO: Type Effectiveness Charts

        # Regional forms
        # We gotta first find what games this can be found in
        # Then we can figure out held items, locations, etc.
        # Evolutions

    def PrintData(self):
        Utils.ClearScreen()

        infoTable = [[colored(f"{self.ENDPOINT.title()}:", attrs=["bold"]), f' {self.PrintName} [{self.ID}]'],
                     self.GetTypeArray()]

        console.print(tabulate(infoTable, tablefmt='plain'))
        self.PrintAbilities()
        self.PrintBaseStats()
        self.PrintVersionInfo()
        return

    def GetTypeArray(self) -> list:
        typeArray = []
        if len(self.types) == 2:
            typeArray.append(colored("Types: ", attrs=["bold"]))
            typeArray.append(f'{self.FormattedTypeOne} / {self.FormattedTypeTwo}')
        else:
            typeArray.append(colored("Type: ", attrs=["bold"]))
            typeArray.append(f'{self.FormattedTypeOne}')

        return typeArray

    def PrintAbilities(self) -> None:
        print()
        if not self.FLAGS['abilities']:
            print("[P]ossible Abilities")
            return

        abilityTable = Table(title="[P]ossible Abilities", box=box.ROUNDED, title_justify='left', show_lines=True)

        abilityTable.add_column("Ability")
        abilityTable.add_column("Description")

        for ability in self.possibleAbilities:
            abilityTable.add_row(f"[bold]{ability.name.title()}[/]", ability.description)
        if self.hiddenAbility is not None:
            abilityTable.add_row(f"[bold](Hidden) {self.hiddenAbility.name.title()}[/]", self.hiddenAbility.description)
        console.print(abilityTable)

    def PrintBaseStats(self) -> None:
        print()
        if not self.FLAGS['stats']:
            print("Base [S]tats")
            return

        # Don't care about hardcoding, this is way more readable
        statsTable = Table(title="Base [S]tats", box=box.ROUNDED, title_justify='left')

        statsTable.add_column("HP", header_style="hp")
        statsTable.add_column("Attack", header_style="attack")
        statsTable.add_column("Defense", header_style="defense")
        statsTable.add_column("Sp Atk", header_style="special-attack")
        statsTable.add_column("Sp Def", header_style="special-defense")
        statsTable.add_column("Speed", header_style="speed")
        statsTable.add_column("Total")

        statsTable.add_row(str(self.baseStats['hp']), str(self.baseStats['attack']),
                           str(self.baseStats['defense']), str(self.baseStats['special-attack']),
                           str(self.baseStats['special-defense']), str(self.baseStats['speed']),
                           str(sum(self.baseStats.values())))

        console.print(statsTable)

    def PrintVersionInfo(self) -> None:
        print()
        if not self.FLAGS['availability']:
            print("[A]vailability Info")
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

        # print("[A]vailability Info (Toggle [U]navailable)")
        # overallInfoTable = Table(title="[A]vailability Info (Toggle [U]navailable)", title_justify="left",
        overallInfoTable = Table(title="[A]vailability Info", title_justify="left", box=box.HORIZONTALS, show_header=False, show_lines=True)

        overallInfoTable.add_column()
        overallInfoTable.add_column()
        overallInfoTable.add_column()

        overallInfoTable.add_row(self.GetGenerationTable(1), self.GetGenerationTable(2), self.GetGenerationTable(3))
        overallInfoTable.add_row(self.GetGenerationTable(4), self.GetGenerationTable(5), self.GetGenerationTable(6))
        overallInfoTable.add_row(self.GetGenerationTable(7), self.GetGenerationTable(8), self.GetGenerationTable(9))

        # TODO: Eventually implement an "ignore certain generations" flag

        console.print(overallInfoTable)

    def GetGenerationTable(self, gen):
        genTable = Table(title=f"Generation {gen}")
        genTable.add_column("Game")
        genTable.add_column("Location")
        genInfo = Generation.Generation.HandleSearch(gen)
        for versionGroup in genInfo.versionGroups:
            groupInfo = VersionGroup.VersionGroup.HandleSearch(versionGroup)
            for version in groupInfo.versions:
                versionLocations = self.locationInformation.get(version)
                if versionLocations is None or len(versionLocations) == 0:
                    continue
                secondCell = ", ".join(versionLocations)
                genTable.add_row(f'[{version}]{Utils.REVERSED_MAPPING_DICT[version]}[/]', secondCell)
        return genTable

    def LocationLoader(self) -> dict[str, list[str]] | None:  # eventually dict[int, list[int]] for IDs instead
        queryURL = f"https://pokemondb.net/pokedex/{self.name}"
        response = requests.get(queryURL)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the table with location information
        locationsDiv = soup.find('div', {'id': 'dex-locations'})

        locationsTable = ''

        # Find the first table after the 'dex-locations' div
        if locationsDiv:
            locationsTable = locationsDiv.find_next('table')

        # Assuming 'location_table' is the BeautifulSoup object for the table
        locationRows = locationsTable.find_all('tr')

        encounters = {}
        for row in locationRows:
            games = []
            locations = []
            gamesHTML = row.find_next('th')
            for game in gamesHTML.find_all('span'):
                games.append(game.text)
            locationsHTML = row.find_next('td')
            for location in locationsHTML.find_all('a'):
                locations.append(location.text)

            for gameName in games:
                encounters[Utils.VERSION_MAPPING_DICT[gameName]] = locations

        return encounters

    @property
    def FormattedTypeOne(self) -> str:
        return f'[{self.types[0]}]{self.types[0].title()}[/]'

    @property
    def FormattedTypeTwo(self) -> str:
        if len(self.types) < 2:
            return ""
        return f'[{self.types[1]}]{self.types[1].title()}[/]'

    # endregion

    def AddToCache(self):
        super().AddToCache()

    @classmethod
    def ToggleFlag(cls, flag: str):
        match flag:
            case 'p':
                cls.FLAGS['abilities'] = not cls.FLAGS['abilities']
            case 's':
                cls.FLAGS['stats'] = not cls.FLAGS['stats']
            case 'a':
                cls.FLAGS['availability'] = not cls.FLAGS['availability']
            case 'u':
                cls.FLAGS['unavailable'] = not cls.FLAGS['unavailable']
            case _:
                return
