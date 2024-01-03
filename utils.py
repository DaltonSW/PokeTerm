import os
import platform
import pickle
import re

import requests

from Resources.data import AbstractData
from console import console
from readchar import readkey, key as keys


# region Version Checks
def IsWindowsOS():
    return platform.system() == "Windows"


def IsLinuxOS():
    return platform.system() == "Linux"


def IsMacOS():
    return platform.system() == "Darwin"


# endregion


# region Visuals
def PrintData(data: AbstractData) -> None:
    while True:
        ClearScreen()
        data.PrintData()
        print()
        console.rule("Press [Enter] to return to the menu.", characters=" ")
        key = readkey()
        if key == keys.ENTER:
            return
        data.ToggleFlag(key)


def ClearScreen(keepHistory=False) -> None:
    if keepHistory:
        console.clear()
        return

    os.system("cls" if IsWindowsOS() else "clear")


# endregion


# region API Access
def GetIDFromURL(URL: str) -> int:
    return int(URL.split("/")[-2])


def NormalizeSearchTerm(searchTerm: str) -> str:
    if str == type(searchTerm):
        searchTerm = re.sub(" ", "-", searchTerm)
    return searchTerm


def GetFromAPI(endpoint, searchTerm):
    searchTerm = NormalizeSearchTerm(searchTerm)
    response = requests.get(f"{BASE_URL}/{endpoint}/{searchTerm}")
    if response.status_code == 404:
        return None
    return response.json()


# If the int being searched on is in the id->name cache, return the proper name. Otherwise, return the original param
def ProperQueryFromID(query: int, idToNameCache) -> str | int:
    return query if query not in idToNameCache else idToNameCache[query]


def GetFromURL(url) -> dict | None:
    response = requests.get(url)
    if response.status_code == 404:
        return None
    return response.json()


# endregion


# region Cache Code
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


# endregion

# region Constants
BASE_URL = "https://pokeapi.co/api/v2"
CACHE_DIR = os.path.expanduser("~") + os.sep + ".poketerm"

VERSION_MAPPING_DICT = {
    "Red": "red",
    "Blue": "blue",
    "Yellow": "yellow",
    "Gold": "gold",
    "Silver": "silver",
    "Crystal": "crystal",
    "Ruby": "ruby",
    "Sapphire": "sapphire",
    "Emerald": "emerald",
    "FireRed": "firered",
    "LeafGreen": "leafgreen",
    "Diamond": "diamond",
    "Pearl": "pearl",
    "Platinum": "platinum",
    "HeartGold": "heartgold",
    "SoulSilver": "soulsilver",
    "Black": "black",
    "White": "white",
    "Colosseum": "colosseum",
    "XD": "xd",
    "Black 2": "black-2",
    "White 2": "white-2",
    "X": "x",
    "Y": "y",
    "Omega Ruby": "omega-ruby",
    "Alpha Sapphire": "alpha-sapphire",
    "Sun": "sun",
    "Moon": "moon",
    "Ultra Sun": "ultra-sun",
    "Ultra Moon": "ultra-moon",
    "Let's Go Pikachu": "lets-go-pikachu",
    "Let's Go Eevee": "lets-go-eevee",
    "Sword": "sword",
    "Shield": "shield",
    "The Isle of Armor": "the-isle-of-armor",
    "The Crown Tundra": "the-crown-tundra",
    "Brilliant Diamond": "brilliant-diamond",
    "Shining Pearl": "shining-pearl",
    "Legends: Arceus": "legends-arceus",
    "Scarlet": "scarlet",
    "Violet": "violet",
    "The Teal Mask": "the-teal-mask",
    "The Indigo Disk": "the-indigo-disk",
}

REVERSED_MAPPING_DICT = {
    "red": "Red",
    "blue": "Blue",
    "yellow": "Yellow",
    "gold": "Gold",
    "silver": "Silver",
    "crystal": "Crystal",
    "ruby": "Ruby",
    "sapphire": "Sapphire",
    "emerald": "Emerald",
    "firered": "FireRed",
    "leafgreen": "LeafGreen",
    "diamond": "Diamond",
    "pearl": "Pearl",
    "platinum": "Platinum",
    "heartgold": "HeartGold",
    "soulsilver": "SoulSilver",
    "black": "Black",
    "white": "White",
    "colosseum": "Colosseum",
    "xd": "XD",
    "black-2": "Black 2",
    "white-2": "White 2",
    "x": "X",
    "y": "Y",
    "omega-ruby": "Omega Ruby",
    "alpha-sapphire": "Alpha Sapphire",
    "sun": "Sun",
    "moon": "Moon",
    "ultra-sun": "Ultra Sun",
    "ultra-moon": "Ultra Moon",
    "lets-go-pikachu": "Let's Go Pikachu",
    "lets-go-eevee": "Let's Go Eevee",
    "sword": "Sword",
    "shield": "Shield",
    "the-isle-of-armor": "The Isle of Armor",
    "the-crown-tundra": "The Crown Tundra",
    "brilliant-diamond": "Brilliant Diamond",
    "shining-pearl": "Shining Pearl",
    "legends-arceus": "Legends: Arceus",
    "scarlet": "Scarlet",
    "violet": "Violet",
    "the-teal-mask": "The Teal Mask",
    "the-indigo-disk": "The Indigo Disk",
}
# endregion
