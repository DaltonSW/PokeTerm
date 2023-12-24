import Utils

class Config:
    PROGRAM_FLAGS = {
        'colorblind': 0,
        'firstLaunch': 1
    }

    POKEMON_FLAGS = {
        'abilities': 1,
        'stats': 1,
        'availability': 0,
        'unavailable': 1,
        'typing': 1,
        'species': 1,
    }

    SPECIES_FLAGS = {}

    TYPE_FLAGS = {
        'efficacy': 1,
        'primary': 0,
        'secondary': 0,
        'moves': 0
    }

    MOVE_FLAGS = {}

    # FLAG_LIST = [
    #     PROGRAM_FLAGS,
    #     SPECIES_FLAGS,
    #     TYPE_FLAGS,
    #     MOVE_FLAGS,
    #     POKEMON_FLAGS
    # ]

    @classmethod
    def LoadCache(cls):
        cache = Utils.LoadCache('config')
        if cache is None:
            return

        cls.PROGRAM_FLAGS = cache['program']
        cls.POKEMON_FLAGS = cache['pokemon']
        # cls.SPECIES_FLAGS = cache['species']
        cls.TYPE_FLAGS = cache['type']
        # cls.MOVE_FLAGS = cache['move']


    @classmethod
    def SaveCache(cls):
        flagList = {
            "program": cls.PROGRAM_FLAGS,
            "pokemon": cls.POKEMON_FLAGS,
            # "species": cls.SPECIES_FLAGS,
            "type": cls.TYPE_FLAGS,
            # "move": cls.MOVE_FLAGS
        }
        Utils.SaveCache('config', flagList)
