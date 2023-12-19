import os
import requests
import pickle
import threading
import time
import re
from Resources.Data import AbstractData

BASE_URL = 'https://pokeapi.co/api/v2'
CACHE_DIR = './cache'


def PrintData(data: AbstractData) -> None:
    data.PrintData()
    print()
    input('Press any key to continue...')


def ClearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def ProperQueryFromID(query: int, idToNameCache) -> str | int:
    if query in idToNameCache:
        return idToNameCache[query]
    else:
        return query


def GetFromAPIWrapper(endpoint, searchTerm):
    stopEvent = threading.Event()
    loadThread = threading.Thread(target=LoadingIndicator, args=[stopEvent])
    loadThread.start()
    response = GetFromAPI(endpoint, searchTerm)
    stopEvent.set()
    loadThread.join()
    return response


def GetFromAPI(endpoint, searchTerm):
    if str == type(searchTerm):
        searchTerm = re.sub(' ', '-', searchTerm)
    response = requests.get(f'{BASE_URL}/{endpoint}/{searchTerm}')
    if response.status_code == 404:
        return None
    return response.json()


def GetFromURL(url):
    response = requests.get(url)
    if response.status_code == 404:
        return None
    return response.json()


def LoadingIndicator(stopEvent: threading.Event):
    ClearScreen()
    numPeriods = 0
    while not stopEvent.is_set():
        numPeriods += 1
        print("Querying PokeAPI" + '.' * numPeriods, end='\r')
        time.sleep(0.33)


def SaveCache(cacheType, cache):
    with open(f'{CACHE_DIR}/{cacheType}.pickle', 'wb') as f:
        pickle.dump(cache, f)
        print(f"Successfully saved {cacheType.upper()} cache")


def LoadCache(cacheType) -> (dict, dict):
    if not os.path.exists(f'{CACHE_DIR}/{cacheType}.pickle'):
        return None
    with open(f'{CACHE_DIR}/{cacheType}.pickle', 'rb') as f:
        cache = pickle.load(f)
        print(f"Successfully loaded {cacheType.upper()} cache")
    return cache
