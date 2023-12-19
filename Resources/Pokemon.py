import Colors
import Utils
from .Data import AbstractData
from tabulate import tabulate
from termcolor import colored, cprint
from . import Species, Ability

ID_TO_NAME_CACHE = {}
NAME_TO_DATA_CACHE = {}
ENDPOINT = 'pokemon'

class Pokemon(AbstractData):
    def __init__(self, data):
        super().__init__()
        global ID_TO_NAME_CACHE
        self.ID: int = data.get('id')
        self.name: str = data.get('name')

        # Abilities
        self.possibleAbilities = []
        self.hiddenAbility = None
        abilityList: list = data.get('abilities')
        for ability in abilityList:
            newAbility = Ability.CheckCaches(ability.get('ability').get('name'))
            if newAbility is None:
                newAbility = Ability.Ability(Utils.GetFromURL(ability.get('ability').get('url')))
                Ability.AddToCache(newAbility)
            if ability.get('get_hidden') is True:
                self.hiddenAbility = newAbility
            else:
                self.possibleAbilities.append(newAbility)

        # Species
        species = Species.CheckCaches(data.get('species').get('name'))
        if species is None:
            species = Species.Species(Utils.GetFromURL(data.get('species').get('url')))
            Species.AddToCache(species)
        self.speciesID = species.ID

        # Stats
        self.baseStats = {}
        self.EVs = {}
        for stat in data.get('stats'):
            statName = stat.get('stat').get('name')
            self.baseStats[statName] = int(stat.get('base_stat'))
            self.EVs[statName] = int(stat.get('effort'))

        # TODO: Set up type information and classes
        self.types = [t.get('type').get('name') for t in data.get('types')]

        # TODO: List what games is available in

        # TODO: Pull other forms

        # TODO: Type Effectiveness Charts

        # TODO: EVs?????

        # Regional forms
        # We gotta first find what games this can be found in
        # Then we can figure out held items, locations, etc
        # EVs given -- Also dunno if this one can even be gotten from PokeAPI?
        # Evolutions

        ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        Utils.ClearScreen()

        infoTable = [[colored(f"{ENDPOINT.title()}:", attrs=["bold"]), f' {self.PrintName} [{self.ID}]'],
                     self.GetTypeArray()]

        print(tabulate(infoTable, tablefmt='plain'))
        self.PrintAbilities()
        self.PrintBaseStats()
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
        print(tabulate(abilityTable, headers=[Colors.GetBoldText('Ability'), Colors.GetBoldText('Description')], tablefmt='rounded_grid'))

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


def HandleSearch() -> Pokemon | None:
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    query = input(f'{ENDPOINT.title()} Name or ID: ').lower()

    if query == '':
        return None

    if query.isdigit():
        query = Utils.ProperQueryFromID(int(query), ID_TO_NAME_CACHE)

    if query in NAME_TO_DATA_CACHE:
        return NAME_TO_DATA_CACHE[query]

    data = Utils.GetFromAPIWrapper(ENDPOINT, query)
    if data is not None:
        newObject = Pokemon(data)
        NAME_TO_DATA_CACHE[newObject.name] = newObject
        return newObject

    return None
