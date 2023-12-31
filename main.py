import os
import shutil
from readchar import readkey, key as keys
from sys import exit

from rich import box
from rich.table import Table

import Utils
from console import console

from Resources import Move, Ability, Type, Version, Pokemon, Species
from Resources import VersionGroup, Generation, Nature, EggGroup
from Config import Config
import Testing
import Updater

# Known Pokemon Edge Cases:
#   Searching Pokemon for "Minior" since apparently they exclusively exist in forms
#   Printing out Eevee's evolutions

# TODO:
#   Once you've got basic information searching working, set up "links" between them
#   Make links "clickable"
#       Ask Discord if I can have clicking a link redirect to a function instead?
#       First just look into the code and see if it can be overridden or something?

BASE_URL = 'https://pokeapi.co/api/v2/'
RESOURCES = {
    'Ability': Ability.Ability,
    # 'Berry': Berry.Berry,
    'EggGroup': EggGroup.EggGroup,
    'Generation': Generation.Generation,
    # 'Item': Item.Item,
    # 'Location': Location.Location,
    'Move': Move.Move,
    'Nature': Nature.Nature,
    'Pokemon': Pokemon.Pokemon,
    'Type': Type.Type,
    'Version': Version.Version,
    'Species': Species.Species,
    'VersionGroup': VersionGroup.VersionGroup,
}

def main():
    LoadCaches()
    printWelcome = True

    if Updater.CheckForUpdate():
        SaveCaches()
        exit(0)

    while True:
        console.clear()
        if printWelcome:
            PrintWelcome()
        # printWelcome = True
        try:
            PrintChoices()
            key = readkey()
            if key == keys.ENTER:
                QuitGracefully()

            console.clear()
            match key:
                # case 'a': HandleSearch(Ability.Ability)
                case 'e': HandleSearch(EggGroup.EggGroup)
                case 'g': HandleSearch(Generation.Generation)
                case 'm': HandleSearch(Move.Move)
                case 'n': HandleSearch(Nature.Nature)
                case 'p': HandleSearch(Pokemon.Pokemon)
                case 'q': Testing.HandleCacheTest()
                case 't': HandleSearch(Type.Type)

                # case '1':
                case '2':
                    ClearCaches()
                case '3':
                    ClearCaches(True)
                case '0':
                    console.clear()
                    exit(0)
                case _:
                    console.print("Not a valid key!")
                    printWelcome = False
                    pass

        except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the menu
            QuitGracefully()

    # TODO:
    #   Location
    #   Item
    #   Game/Version
    #   PokeBalls
    #   Catch Rate Calculator

def PrintChoices():
    print()
    console.rule("[bold white]Press a bracketed letter to search on that topic.", characters=' ')
    console.rule("[bold white]Press Enter to save caches and exit.", characters=' ')

    overallTable = Table(show_header=False, box=box.SIMPLE)

    searchOptions = [
        # "[A]bility",
        # "[B]erry",
        # "[C]alculators",
        "[E]gg Groups",
        "[G]eneration",
        # "[I]tem",
        # "[L]ocation",
        "[M]ove",
        "[N]ature",
        "[P]okemon",
        "[T]ype"
        ]

    adminOptions = [
        # "[1] Options",
        "[2] Clear Cache",
        "[3] Clear Cache & Quit",
        "[0] Quit Without Saving",
        # "[Enter] Save & Quit"
    ]

    searchTable, adminTable = Table(show_header=False, box=box.SIMPLE), Table(show_header=False, box=box.SIMPLE)

    for option in searchOptions:
        searchTable.add_row(f'[bold]{option}[/]')

    for option in adminOptions:
        adminTable.add_row(f'[bold]{option}[/]')

    overallTable.add_row(searchTable, adminTable)

    console.print(overallTable, justify='center')
    console.rule("[bold white]\[Enter] Save & Quit[/]", characters=' ')

def PrintWelcome():
    console.rule('[red]     #########    [/]', characters=' ')
    console.rule('[red]   #############  [/]', characters=' ')
    console.rule('[red]  ############### [/]', characters=' ')
    console.rule('[red] #####       #####[/]', characters=' ')
    console.rule('[white]        ###       [/]', characters=' ')
    console.rule('[white]        ###       [/]', characters=' ')
    console.rule('[white] #####       #####[/]', characters=' ')
    console.rule('[white]  ############### [/]', characters=' ')
    console.rule('[white]   #############  [/]', characters=' ')
    console.rule('[white]     #########    [/]', characters=' ')
    print()
    console.rule(f"[bold white]Welcome to [red]Poké[/]Term!", style='white')
    console.rule(f"Cache is stored at ~{os.sep}.poketerm", characters=' ')

def HandleSearch(resource):
    query = input(f'{resource.ENDPOINT.title()} Name or ID: ').lower()
    if query == '':
        return

    with console.status(f"Querying for {resource.ENDPOINT.title()}..."):
        result = resource.HandleSearch(query)
    if result is not None:
        Utils.PrintData(result)
    return

def SaveCaches():
    if not os.path.exists(Utils.CACHE_DIR):
        os.makedirs(Utils.CACHE_DIR)
    for resource in RESOURCES.values():
        resource.SaveCache()

    Config.SaveCache()

def LoadCaches():
    for resource in RESOURCES.values():
        resource.LoadCache()

    Config.LoadCache()
    console.clear()

def ClearCaches(doQuit=False):
    if os.path.exists(Utils.CACHE_DIR):
        shutil.rmtree(Utils.CACHE_DIR)

    for resource in RESOURCES.values():
        resource.NAME_TO_DATA_CACHE.clear()
        resource.ID_TO_NAME_CACHE.clear()

    if doQuit:
        exit(0)

def QuitGracefully():
    SaveCaches()
    console.clear()
    exit(0)

if __name__ == '__main__':
    main()
