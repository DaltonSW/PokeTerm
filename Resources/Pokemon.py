import time

import Colors
import Utils
from Resources.Data import AbstractData
from tabulate import tabulate
from termcolor import colored, cprint
from Resources import Species, Ability


class Pokemon(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'pokemon'

    def __init__(self, data):
        super().__init__(data)

        # Abilities
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

        # TODO: Pivot this to the PokeDB scraper
        # Available Locations
        # encountersURL = data.get('location_area_encounters')
        # encountersData = Utils.GetFromURL(encountersURL)
        # self.availableVersions = {}
        # for encounter in encountersData:
        #     location = encounter.get('location_area').get('name')
        #     version = encounter.get('version_details')[0].get('version').get('name')
        #     self.availableVersions[version] = 1
        #     method = encounter.get('version_details')[0].get('encounter_details')[0].get('method').get('name')
        #     level = encounter.get('version_details')[0].get('encounter_details')[0].get('level')
        #     # print(f"Location: {location}, Version: {version}, Method: {method}, Level: {level}")

        # TODO: Set up type information and classes
        self.types = [t.get('type').get('name') for t in data.get('types')]

        # TODO: List what games is available in

        # TODO: Pull other forms

        # TODO: Type Effectiveness Charts

        # Regional forms
        # We gotta first find what games this can be found in
        # Then we can figure out held items, locations, etc.
        # EVs given -- Also dunno if this one can even be gotten from PokeAPI?
        # Evolutions

    def PrintData(self):
        Utils.ClearScreen()

        infoTable = [[colored(f"{self.ENDPOINT.title()}:", attrs=["bold"]), f' {self.PrintName} [{self.ID}]'],
                     self.GetTypeArray()]

        print(tabulate(infoTable, tablefmt='plain'))
        self.PrintAbilities()
        self.PrintBaseStats()
        # self.PrintAvailableVersions()
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
        cprint("Possible Abilities:", attrs=["bold"])
        abilityTable = []
        for ability in self.possibleAbilities:
            abilityTable.append([colored(f"{ability.name.title()}", attrs=["bold"]), ability.description])
        if self.hiddenAbility is not None:
            abilityTable.append([colored(f"(Hidden) {self.hiddenAbility.name.title()}", attrs=["bold"])])
        print(tabulate(abilityTable, headers=[Colors.GetBoldText('Ability'), Colors.GetBoldText('Description')],
                       tablefmt='rounded_grid'))

    def PrintBaseStats(self) -> None:
        print()
        cprint("Base Stats:", attrs=["bold"])
        stats = {}
        total = 0
        for stat, value in self.baseStats.items():
            color, name = Colors.GetStatFormatting(stat)
            stats[colored(name, color=color)] = [value]
            total += value

        stats["Total"] = [total]

        print(tabulate(stats, headers='keys', tablefmt='rounded_grid', numalign='center', stralign='center'))

    # def PrintAvailableVersions(self) -> None:
    #     print()
    #     print("Available Versions:")
    #     for version in self.availableVersions.keys():
    #         print(version)

    # region Formatted Getters
    # @property
    # def FormattedResourceProperty(self) -> str:
    #     return colored(self.property.title(), Colors.GetWhateverColor(self.property))

    @property
    def FormattedTypeOne(self) -> str:
        return colored(self.types[0].title(), Colors.GetTypeColor(self.types[0]))

    @property
    def FormattedTypeTwo(self) -> str:
        if len(self.types) < 2:
            return ""
        return colored(self.types[1].title(), Colors.GetTypeColor(self.types[1]))

    # endregion

    def AddToCache(self):
        super().AddToCache()

def CacheTest():
    NAME_TO_DATA_CACHE = {}
    ID_TO_NAME_CACHE = {}
    for i in range(1, 152):
        data = Utils.GetFromAPI('pokemon', i)
        if data is not None:
            newObject = Pokemon(data)
            NAME_TO_DATA_CACHE[newObject.name] = newObject
            ID_TO_NAME_CACHE[newObject.ID] = newObject.name
        print(f"Processed {i}")
        time.sleep(1)
    Pokemon.SaveCache()
