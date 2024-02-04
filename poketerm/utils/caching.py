import os
import shutil
import pickle


class SubCache:
    NAME_TO_ID = {}
    ID_TO_DATA = {}


class CacheManager:
    cache_mappings: dict[str, SubCache] = {}

    @classmethod
    def add_name_to_ID_mapping(cls, key, name, ID):
        cls.cache_mappings.setdefault(key, SubCache()).NAME_TO_ID[name] = ID

    @classmethod
    def add_ID_to_data_mapping(cls, key, ID, data):
        cls.cache_mappings.setdefault(key, SubCache()).ID_TO_DATA[ID] = data

    @classmethod
    def get_ID_from_name(cls, key, name):
        subcache = cls.cache_mappings.get(key, None)
        if not subcache:
            return None
        return subcache.NAME_TO_ID.get(name)

    @classmethod
    def get_data_from_ID(cls, key, ID):
        subcache = cls.cache_mappings.get(key, None)
        if not subcache:
            return None
        return subcache.ID_TO_DATA.get(ID)

    @classmethod
    def get_data_from_name(cls, key, name):
        subcache = cls.cache_mappings.get(key, None)
        if not subcache:
            return None
        ID = subcache.NAME_TO_ID.get(name, None)
        if not ID:
            return None
        return subcache.ID_TO_DATA.get(ID, None)

    @classmethod
    def save_caches(cls):
        verify_cache_dir()
        with open(get_cache_filepath("mappings"), "wb") as cache_file:
            pickle.dump(cls.cache_mappings, cache_file)

    @classmethod
    def load_caches(cls):
        if not does_cache_type_exist("mappings"):
            return None
        with open(get_cache_filepath("mappings"), "wb") as cache_file:
            cls.cache_mappings = pickle.load(cache_file)


def get_cache_dir():
    return os.path.join(os.path.expanduser("~"), os.sep, ".poketerm")


def get_cache_filepath(cacheType) -> str:
    return os.path.join(get_cache_dir(), f"{cacheType}.cache")


# Checks if the cache directory exists. Creates it if it doesn't
def verify_cache_dir():
    if not os.path.exists(get_cache_dir()):
        os.makedirs(get_cache_dir())


def remove_cache_dir():
    if os.path.exists(get_cache_dir()):
        shutil.rmtree(get_cache_dir())


def does_cache_type_exist(cacheType) -> bool:
    return os.path.exists(get_cache_filepath(cacheType))


def save_cache(cacheType, cache) -> None:
    with open(get_cache_filepath(cacheType), "wb") as f:
        pickle.dump(cache, f)
        print(f"Successfully saved {cacheType.upper()} cache")


def load_cache(cacheType) -> dict | None:
    if not does_cache_type_exist(cacheType):
        return None
    with open(get_cache_filepath(cacheType), "rb") as f:
        cache = pickle.load(f)
        print(f"Successfully loaded {cacheType.upper()} cache")
    return cache
