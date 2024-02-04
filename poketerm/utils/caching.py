import os
import shutil
import pickle


class SubCache:
    NAME_TO_ID = {}
    ID_TO_DATA = {}


class CacheManager:
    # Will map some arbitrary string as a key
    # CacheMappings["unique-key"] = SubCache
    cache_mappings: dict[str, SubCache] = {}

    @classmethod
    def add_to_name_cache(cls, key, name, ID):
        cls.cache_mappings.setdefault(key, SubCache()).NAME_TO_ID[name] = ID

    @classmethod
    def add_to_ID_cache(cls, key, ID, data):
        cls.cache_mappings.setdefault(key, SubCache()).ID_TO_DATA[ID] = data

    @classmethod
    def get_ID_from_name(cls, key, name):
        subcache = cls.cache_mappings.get(key, None)
        if subcache:
            return subcache.NAME_TO_ID.get(name)

    @classmethod
    def get_data_from_name(cls, key, name):
        subcache = cls.cache_mappings.get(key, None)
        if not subcache:
            return None
        ID = subcache.NAME_TO_ID.get(name, None)
        if ID:
            return subcache.ID_TO_DATA.get(ID, None)

    @classmethod
    def get_data_from_ID(cls, key, ID):
        subcache = cls.cache_mappings.get(key, None)
        if subcache:
            return subcache.ID_TO_DATA.get(ID)


def CacheDirectory():
    return os.path.join(os.path.expanduser("~"), os.sep, ".poketerm")


def CacheFilePath(cacheType) -> str:
    return os.path.join(CacheDirectory(), f"{cacheType}.cache")


def VerifyCacheDir():
    if not os.path.exists(CacheDirectory()):
        os.makedirs(CacheDirectory())


def RemoveCacheDir():
    if os.path.exists(CacheDirectory()):
        shutil.rmtree(CacheDirectory())


def CacheExists(cacheType) -> bool:
    return os.path.exists(CacheFilePath(cacheType))


def SaveCache(cacheType, cache) -> None:
    with open(CacheFilePath(cacheType), "wb") as f:
        pickle.dump(cache, f)
        print(f"Successfully saved {cacheType.upper()} cache")


def LoadCache(cacheType) -> dict | None:
    if not CacheExists(cacheType):
        return None
    with open(CacheFilePath(cacheType), "rb") as f:
        cache = pickle.load(f)
        print(f"Successfully loaded {cacheType.upper()} cache")
    return cache
