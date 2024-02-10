import os
import shutil
import pickle


class MappingCache:
    def __init__(self):
        self.NAME_TO_ID = {}
        self.ID_TO_DATA = {}


class CacheManager:
    resource_mappings: dict[str, MappingCache] = {}

    @classmethod
    def add_name_to_ID_mapping(cls, key, name, ID):
        cls.resource_mappings.setdefault(key, MappingCache()).NAME_TO_ID[name] = ID

    @classmethod
    def add_ID_to_data_mapping(cls, key, ID, data):
        cls.resource_mappings.setdefault(key, MappingCache()).ID_TO_DATA[ID] = data

    @classmethod
    def get_ID_from_name(cls, key, name):
        subcache = cls.resource_mappings.get(key, None)
        if not subcache:
            return None
        return subcache.NAME_TO_ID.get(name)

    @classmethod
    def get_data_from_ID(cls, key, ID):
        subcache = cls.resource_mappings.get(key, None)
        if not subcache:
            return None
        return subcache.ID_TO_DATA.get(int(ID))

    @classmethod
    def get_data_from_name(cls, key, name):
        subcache = cls.resource_mappings.get(key, None)
        if not subcache:
            return None
        ID = subcache.NAME_TO_ID.get(name, None)
        if not ID:
            return None
        return subcache.ID_TO_DATA.get(ID, None)

    @classmethod
    def save_mappings(cls):
        if cls.resource_mappings == {}:
            return
        cls.save_cache_of_type("mappings", cls.resource_mappings)

    @classmethod
    def load_mappings(cls):
        cls.resource_mappings = cls.load_cache_of_type("mappings")
        if cls.resource_mappings is None:
            cls.resource_mappings = {}

    @classmethod
    def clear_mappings(cls):
        cls.resource_mappings = {}
        cls.clear_cache_of_type("mappings")

    @staticmethod
    def save_cache_of_type(cache_type: str, cache):
        verify_cache_dir()

        with open(get_cache_filepath(cache_type), "wb") as cache_file:
            cache_file.write(pickle.dumps(cache))

    @staticmethod
    def load_cache_of_type(cache_type: str):
        if not does_cache_type_exist(cache_type):
            return None
        if not os.path.getsize(get_cache_filepath(cache_type)) > 0:
            return None
        with open(get_cache_filepath(cache_type), "rb") as cache_file:
            data = pickle.load(cache_file)
        return data

    @staticmethod
    def clear_cache_of_type(cache_type: str):
        if not does_cache_type_exist(cache_type):
            return None
        os.remove(get_cache_filepath(cache_type))

    @classmethod
    def cache_resource(cls, resource):
        if resource is None:
            return
        cls.add_name_to_ID_mapping(resource.ENDPOINT, resource.name, resource.ID)
        cls.add_ID_to_data_mapping(resource.ENDPOINT, resource.ID, resource)


def get_cache_dir():
    return os.path.join(os.path.expanduser("~"), ".poketerm")


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
