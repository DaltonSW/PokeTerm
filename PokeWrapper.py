import Utils
from Resources import Move, Ability, Type, Version, Pokemon

class PokeWrapper:
    BASE_URL = 'https://pokeapi.co/api/v2/'

    @classmethod
    def HandleSearch(cls, optionName):
        match optionName:
            case 'Pokemon':
                result = Pokemon.HandleSearch()
            case 'Ability':
                result = Ability.HandleSearch()
            case 'Type':
                result = Type.HandleSearch()
            case 'Move':
                result = Move.HandleSearch()
            case 'Berry':
                return
            case 'Location':
                return
            case 'Item':
                return
            case 'Version':
                result = Version.HandleSearch()
            case _:
                result = "Not a valid search!"
        Utils.PrintData(result)

    @staticmethod
    def SaveCaches():
        Pokemon.SaveCache()
        Ability.SaveCache()
        Type.SaveCache()
        Move.SaveCache()
        # Berry.SaveCache()
        # Location.SaveCache()
        # Item.SaveCache()
        Version.SaveCache()

    @staticmethod
    def LoadCaches():
        Pokemon.LoadCache()
        Ability.LoadCache()
        Type.LoadCache()
        Move.LoadCache()
        # Berry.LoadCache()
        # Location.LoadCache()
        # Item.LoadCache()
        Version.LoadCache()
