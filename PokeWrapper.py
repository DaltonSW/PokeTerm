import Utils
from Resources import Move, Ability, Type, Version, Pokemon

class PokeWrapper:
    BASE_URL = 'https://pokeapi.co/api/v2/'

    @classmethod
    def HandleSearch(cls, optionName):
        match optionName:
            case 'Pokemon':
                return
            case 'Ability':
                result = Ability.HandleSearch()
            case 'Type':
                return
            case 'Move':
                result = Move.HandleSearch()
            case 'Berry':
                return
            case 'Location':
                return
            case 'Item':
                return
            case 'Version':
                return
            case _:
                result = "Not a valid search!"
        Utils.PrintData(result)

    @staticmethod
    def SaveCaches():
        Move.SaveCache()

    @staticmethod
    def LoadCaches():
        Move.LoadCache()
