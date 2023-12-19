import os

import Utils
from Resources import Move, Ability, Type, Version, Pokemon, Species

class PokeWrapper:
    BASE_URL = 'https://pokeapi.co/api/v2/'

    RESOURCES = {
        'Pokemon': Pokemon,
        'Ability': Ability,
        'Type': Type,
        'Move': Move,
        'Version': Version,
        # 'Berry': Berry,
        # 'Location': Location,
        # 'Item': Item,
        'Species': Species,
    }

    @classmethod
    def HandleSearch(cls, optionName):
        resource = cls.RESOURCES.get(optionName)
        if resource is not None:
            result = resource.HandleSearch()
            if result is not None:
                Utils.PrintData(result)
        else:
            print("Not a valid search!")

    @staticmethod
    def SaveCaches():
        if not os.path.exists(Utils.CACHE_DIR):
            os.makedirs(Utils.CACHE_DIR)
        for resource in PokeWrapper.RESOURCES.values():
            resource.SaveCache()

    @staticmethod
    def LoadCaches():
        for resource in PokeWrapper.RESOURCES.values():
            resource.LoadCache()
