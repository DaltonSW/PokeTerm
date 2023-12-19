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
    """
    Prints the data from the object of type 'Data'. In the end, it waits for the user to press any key to continue.

    Args:
        data (AbstractData): An object of type 'Data' containing data to be printed.
    """
    data.PrintData()
    print()
    input('Press any key to continue...')

def ClearScreen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ProperQueryFromID(query: int, idToNameCache) -> str | int:
    """
    Returns the proper query based on the given ID.

    Args:
        query (str): The ID of the query.
        idToNameCache (dict): A dictionary containing ID to name mappings.

    Returns:
        str: The proper query if it exists in the cache, else the original query.
    """
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
    """
    Queries the API and returns the response.

    Args:
        endpoint (str): The endpoint of the API to query. E.g. "pokemon", "ability", etc.
        searchTerm (str): The term to search for within the specified endpoint. E.g. "pikachu", "3", "overgrow", etc.

    Returns:
        dict or None: The JSON response from the API if the request is successful, None if the response status code is 404.
    """
    searchTerm = re.sub(' ', '-', searchTerm)
    response = requests.get(f'{BASE_URL}/{endpoint}/{searchTerm}')
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
    """
    Saves the specified cache object.

    Args:
        cacheType (str): The type of cache being saved.
        cache (Any serializable object): The cache object to be saved.
    """
    with open(f'{CACHE_DIR}/{cacheType}.pickle', 'wb') as f:
        pickle.dump(cache, f)
        print(f"Successfully saved {cacheType.upper()} cache")

def LoadCache(cacheType) -> (dict, dict):
    """
    Loads the cache data from the specified cache file.

    Args:
        cacheType (str): The type of cache to load. Generally, this is <resource_name>.lower()

    Returns:
        dict or None: The loaded cache if file exists, None otherwise.
    """
    if not os.path.exists(f'{CACHE_DIR}/{cacheType}.pickle'):
        return None
    with open(f'{CACHE_DIR}/{cacheType}.pickle', 'rb') as f:
        cache = pickle.load(f)
        print(f"Successfully loaded {cacheType.upper()} cache")
    return cache
