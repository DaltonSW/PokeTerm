import Utils
from .Data import AbstractData
from Resources import EvolutionChain
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
        self.catchRate: int = data.get('capture_rate')

        # PokeDex Numbers
        pokedexData = data.get('pokedex_numbers')
        self.pokedexNumbers = {}
        for entry in pokedexData:
            self.pokedexNumbers[entry['pokedex']['name']] = entry['entry_number']

        # Evolution Chain
        self.evolutionChain = EvolutionChain.EvolutionChain(Utils.GetFromURL(data.get('evolution_chain').get('url')))

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        self.evolutionChain.PrintData()
        return

    def AddToCache(self):
        super().AddToCache()

    @property
    def GenderRatio(self) -> str:
        if self.genderRatio == -1:
            return 'Genderless'

        if self.genderRatio == 0:
            return '[male]100%[/] male'

        if self.genderRatio == 8:
            return '[female]100%[/] female'

        return f'[female]{self.genderRatio * 12.5}%[/] female / [male]{(8 - self.genderRatio) * 12.5}%[/] male'

    # Formula gotten from Smogon guide, originally from forum user X-Act
    # https://www.smogon.com/ingame/guides/capture_mechanics
    @property
    def CaptureRate(self) -> str:
        maxHP = 100
        ballRate = 1  # 1 is Pokeball, 1.5 for Great, 2 for Ultra
        status = 1  # 1 is None, 1.5 is poison, burn, or paralysis, 2 is sleep or freeze
        captureRate = float(((1 + (maxHP * 3 - maxHP * 2) * self.catchRate * ballRate * status) / (maxHP * 3)) / 256)

        return str(f"{self.catchRate} (~{(captureRate * 100):.2f}% in PokeBall @ full HP)")

    @property
    def HatchCycles(self) -> str:
        return f"{str(self.hatchCycles)} ({(self.hatchCycles * 128):,} - {(self.hatchCycles * 257):,} steps)"

    @property
    def EggGroups(self) -> str:
        return ', '.join(group.title() for group in self.eggGroups)

    @property
    def GrowthRate(self) -> str:
        match self.growthRate:
            case 'erratic':
                return 'Erratic (Lvl 100: 600,000 XP)'
            case 'fast':
                return 'Fast (Lvl 100: 800,000 XP)'
            case 'medium-fast':
                return 'Medium Fast (Lvl 100: 1,000,000 XP)'
            case 'medium-slow':
                return 'Medium Slow (Lvl 100: 1,059,860 XP)'
            case 'slow':
                return 'Slow (Lvl 100: 1,250,000 XP)'
            case 'fluctuating':
                return 'Fluctuating (Lvl 100: 1,640,000 XP)'

        return str(self.growthRate)

    def PrintDataForPokemonPage(self):
        infoTable = Table(show_header=False, box=box.ROUNDED, show_lines=True)

        infoTable.add_column("Gender/EggGroups/Happiness", ratio=2)
        infoTable.add_column("#s", ratio=3)
        infoTable.add_column("CaptureRate/HatchCycles/GrowthRate", ratio=2)
        infoTable.add_column("Values", ratio=5)

        infoTable.add_row('[b]Gender Ratio:[/]', self.GenderRatio, '[b]Capture Rate:[/]', self.CaptureRate)
        infoTable.add_row('[b]Egg Groups:[/]', self.EggGroups, '[b]Hatch Cycles:[/]', self.HatchCycles)
        # infoTable.add_row('Base Happiness', str(self.baseHappiness), 'EXP Growth Rate', self.GrowthRate)
        infoTable.add_row('[b]EXP Growth Rate:[/]', self.GrowthRate, '[b]Base Happiness:[/]', str(self.baseHappiness))

        console.print(infoTable)
