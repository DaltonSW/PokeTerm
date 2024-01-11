import os
import pickle

CACHE_DIR = os.path.expanduser("~") + os.sep + ".poketerm"


def CacheFilePath(cacheType) -> str:
    return os.path.join(CACHE_DIR, f"{cacheType}.cache")


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
