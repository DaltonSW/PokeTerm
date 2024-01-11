import os
import shutil
import pickle


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
