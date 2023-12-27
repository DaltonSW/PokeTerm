import os
import shutil
import requests
import pickle
import re
import getch
from Resources.Data import AbstractData

BASE_URL = 'https://pokeapi.co/api/v2'
CACHE_DIR = './cache'

LOADED_THIS_SESSION = set()

def PrintData(data: AbstractData) -> None:
    while True:
        ClearScreen()
        data.PrintData()
        print()
        print('Press any bracketed letter to expand/collapse the section. Press "Enter" to return.')
        key = getch.getch()
        if key == os.linesep[0]:
            return
        data.ToggleFlag(key)


def ClearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ClearCache():
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)


def GetIDFromURL(URL: str) -> int:
    return int(URL.split('/')[-2])


def ProperQueryFromID(query: int, idToNameCache) -> str | int:
    if query in idToNameCache:
        return idToNameCache[query]
    else:
        return query


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


def SaveCache(cacheType, cache):
    with open(f'{CACHE_DIR}/{cacheType}.cache', 'wb') as f:
        pickle.dump(cache, f)
        print(f"Successfully saved {cacheType.upper()} cache")


def LoadCache(cacheType) -> (dict, dict):
    if not os.path.exists(f'{CACHE_DIR}/{cacheType}.cache'):
        return None
    with open(f'{CACHE_DIR}/{cacheType}.cache', 'rb') as f:
        cache = pickle.load(f)
        print(f"Successfully loaded {cacheType.upper()} cache")
    return cache

# region Constants

VERSION_MAPPING_DICT = {
    'Red': 'red',
    'Blue': 'blue',
    'Yellow': 'yellow',
    'Gold': 'gold',
    'Silver': 'silver',
    'Crystal': 'crystal',
    'Ruby': 'ruby',
    'Sapphire': 'sapphire',
    'Emerald': 'emerald',
    'FireRed': 'firered',
    'LeafGreen': 'leafgreen',
    'Diamond': 'diamond',
    'Pearl': 'pearl',
    'Platinum': 'platinum',
    'HeartGold': 'heartgold',
    'SoulSilver': 'soulsilver',
    'Black': 'black',
    'White': 'white',
    'Colosseum': 'colosseum',
    'XD': 'xd',
    'Black 2': 'black-2',
    'White 2': 'white-2',
    'X': 'x',
    'Y': 'y',
    'Omega Ruby': 'omega-ruby',
    'Alpha Sapphire': 'alpha-sapphire',
    'Sun': 'sun',
    'Moon': 'moon',
    'Ultra Sun': 'ultra-sun',
    'Ultra Moon': 'ultra-moon',
    "Let's Go Pikachu": 'lets-go-pikachu',
    "Let's Go Eevee": 'lets-go-eevee',
    'Sword': 'sword',
    'Shield': 'shield',
    "The Isle of Armor": 'the-isle-of-armor',
    "The Crown Tundra": 'the-crown-tundra',
    'Brilliant Diamond': 'brilliant-diamond',
    'Shining Pearl': 'shining-pearl',
    'Legends: Arceus': 'legends-arceus',
    'Scarlet': 'scarlet',
    'Violet': 'violet',
    "The Teal Mask": "the-teal-mask",
    "The Indigo Disk": "the-indigo-disk"
}

REVERSED_MAPPING_DICT = {
    'red': 'Red',
    'blue': 'Blue',
    'yellow': 'Yellow',
    'gold': 'Gold',
    'silver': 'Silver',
    'crystal': 'Crystal',
    'ruby': 'Ruby',
    'sapphire': 'Sapphire',
    'emerald': 'Emerald',
    'firered': 'FireRed',
    'leafgreen': 'LeafGreen',
    'diamond': 'Diamond',
    'pearl': 'Pearl',
    'platinum': 'Platinum',
    'heartgold': 'HeartGold',
    'soulsilver': 'SoulSilver',
    'black': 'Black',
    'white': 'White',
    'colosseum': 'Colosseum',
    'xd': 'XD',
    'black-2': 'Black 2',
    'white-2': 'White 2',
    'x': 'X',
    'y': 'Y',
    'omega-ruby': 'Omega Ruby',
    'alpha-sapphire': 'Alpha Sapphire',
    'sun': 'Sun',
    'moon': 'Moon',
    'ultra-sun': 'Ultra Sun',
    'ultra-moon': 'Ultra Moon',
    'lets-go-pikachu': "Let's Go Pikachu",
    'lets-go-eevee': "Let's Go Eevee",
    'sword': 'Sword',
    'shield': 'Shield',
    'the-isle-of-armor': "The Isle of Armor",
    'the-crown-tundra': "The Crown Tundra",
    'brilliant-diamond': 'Brilliant Diamond',
    'shining-pearl': 'Shining Pearl',
    'legends-arceus': 'Legends: Arceus',
    'scarlet': 'Scarlet',
    'violet': 'Violet',
    'the-teal-mask': "The Teal Mask",
    'the-indigo-disk': "The Indigo Disk"
}
# endregion
