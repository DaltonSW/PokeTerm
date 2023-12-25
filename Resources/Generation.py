from Resources.Data import AbstractData

# TODO:
#   List out each ability
#   List out each move
#   List out each Species added

class Generation(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'generation'

    def __init__(self, data):
        super().__init__(data)

        self.abilitiesIntroduced: list[str] = [thing['name'] for thing in data['abilities']]
        self.movesIntroduced: list[str] = [thing['name'] for thing in data['moves']]
        self.speciesIntroduced: list[str] = [thing['name'] for thing in data['pokemon_species']]

        self.versionGroups: list[str] = [thing['name'] for thing in data['version_groups']]

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        print()
        print(f"Generation {self.ID}")
        print(f'Abilities Introduced: {len(self.abilitiesIntroduced)}')
        print(f'Moves Introduced: {len(self.movesIntroduced)}')
        print(f'Species Introduced: {len(self.speciesIntroduced)}')

        pass

    def __str__(self):
        return ''

    def AddToCache(self):
        super().AddToCache()
