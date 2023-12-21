import Utils
from .Data import AbstractData
from console import console
from rich.table import Table
from rich import box


class Species(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'pokemon-species'

    def __init__(self, data):
        super().__init__(data)

        # Colors, Egg Groups, Evolution Chains, Pokedexes, and Shapes COULD all be their own classes/endpoint
        # Physical identifiers
        self.shape: str = data.get('shape').get('name')
        self.color: str = data.get('color').get('name')

        # Egg information
        self.eggGroups: list[str] = [group['name'] for group in data.get('egg_groups')]
        self.hatchCycles: int = data.get('hatch_counter')
        self.genderRatio: float = data.get(
            'gender_rate')  # "Chance of this pokemon being female, in eights. -1 if genderless"

        # Misc Information
        self.growthRate: str = data.get('growth_rate').get('name')
        self.baseHappiness: int = data.get('base_happiness')
        self.captureRate: int = data.get('capture_rate')

        pokedexData = data.get('pokedex_numbers')
        self.pokedexNumbers = {}
        for entry in pokedexData:
            self.pokedexNumbers[entry['pokedex']['name']] = entry['entry_number']

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):

        return

    def AddToCache(self):
        super().AddToCache()

    @property
    def GenderRatio(self) -> str:
        return str(self.genderRatio)

    @property
    def CaptureRate(self) -> str:
        return str(self.captureRate)

    @property
    def HatchCycles(self) -> str:
        return str(self.hatchCycles)

    @property
    def EggGroups(self) -> str:
        return ', '.join(self.eggGroups)

    @property
    def GrowthRate(self) -> str:
        return str(self.growthRate)

    def PrintDataForPokemonPage(self):
        infoTable = Table(show_header=False, box=box.SIMPLE)

        infoTable.add_column("Gender/Capture", ratio=3)
        infoTable.add_column("#s", ratio=1)
        infoTable.add_column("Groups/Cycles", ratio=3)
        infoTable.add_column("#s", ratio=1)
        infoTable.add_column("Growth/Happiness", ratio=3)
        infoTable.add_column("#s", ratio=3)

        infoTable.add_row('Gender Ratio', self.GenderRatio, 'Hatch Cycles', self.HatchCycles,
                          'Egg Groups', self.EggGroups)
        infoTable.add_row('Capture Rate', self.CaptureRate, 'Base Happiness', str(self.baseHappiness),
                          'EXP Growth Rate', self.GrowthRate)

        console.print(infoTable)
