import os
import pickle
import requests
import pickle
from Resources import Move

class PokeWrapper:
    BASE_URL = 'https://pokeapi.co/api/v2/'

    @classmethod
    def HandleSearch(cls, optionName):
        match optionName:
            case 'Pokemon':
                return
            case 'Ability':
                return
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
        print(result)

    @classmethod
    def PokemonSearch(cls):
        return

    @classmethod
    def SaveCaches(cls):
        Move.SaveCache()

    @classmethod
    def LoadCaches(cls):
        Move.LoadCache()
