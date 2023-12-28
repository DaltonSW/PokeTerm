from console import console
from Resources.Data import AbstractData

class Nature(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'nature'

    def __init__(self, data):
        super().__init__(data)

        self.decreasedStat = data.get('decreased_stat').get('name')
        self.increasedStat = data.get('increased_stat').get('name')
        self.hatesFlavor = data.get('hates_flavor').get('name')
        self.likesFlavor = data.get('likes_flavor').get('name')

        # also has move_battle_style_preferences and pokeathlon_stat_changes

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        print()
        console.rule(f"[bold]{self.PrintName}", align='left', style='none')
        console.print(f'[attack]Increased Stat: [/]{self.increasedStat.title()}')
        console.print(f'[defense]Decreased Stat: [/]{self.decreasedStat.title()}')
        print()
        console.print(f'[attack]Likes Flavor: [/]{self.likesFlavor.title()}')
        console.print(f'[defense]Hates Flavor: [/]{self.hatesFlavor.title()}')
        pass

    def __str__(self):
        return ''

    def AddToCache(self):
        super().AddToCache()
