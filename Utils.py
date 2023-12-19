import os
import requests
import pickle

BASE_URL = 'https://pokeapi.co/api/v2'
CACHE_DIR = './cache'

def ProperQueryFromID(query, idToNameCache):
    if query in idToNameCache:
        return idToNameCache[query]
    else:
        return query

def GetFromAPI(endpoint, searchTerm):
    print("Querying PokeAPI...")
    response = requests.get(f'{BASE_URL}/{endpoint}/{searchTerm}')
    if response.status_code == 404:
        return None
    return response.json()

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
