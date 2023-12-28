import os
import shutil
from sys import exit

from rich import box
from rich.table import Table

import Utils
from console import console
from rich.progress import track

from Resources import Move, Ability, Type, Version, Pokemon, Species
from Resources import VersionGroup, Generation, Nature
from Config import Config

# Known Pokemon Edge Cases:
#   Searching Pokemon for "Minior" since apparently they exclusively exist in forms
#   Printing out Eevee's evolutions

# TODO:
#   Once you've got basic information searching working, set up "links" between them
#   Make links "clickable"
#       Ask Discord if I can have clicking a link redirect to a function instead?
#       First just look into the code and see if it can be overridden or something?

VERSION = "0.1.2"

BASE_URL = 'https://pokeapi.co/api/v2/'
RESOURCES = {
    'Pokemon': Pokemon.Pokemon,
    'Ability': Ability.Ability,
    'Type': Type.Type,
    'Move': Move.Move,
    'Version': Version.Version,
    # 'Berry': Berry.Berry,
    # 'Location': Location.Location,
    # 'Item': Item.Item,
    'Species': Species.Species,
    'VersionGroup': VersionGroup.VersionGroup,
    'Generation': Generation.Generation,
    'Nature': Nature.Nature
}

def main():
    LoadCaches()
    printWelcome = True

    while True:
        Utils.ClearScreen()
        if printWelcome: PrintWelcome()
        # printWelcome = True
        try:
            PrintChoices()
            key = Utils.GetChar()
            if key == '\r':
                QuitGracefully()

            Utils.ClearScreen()
            match key:
                # case 'a': HandleSearch(Ability.Ability)
                case 'g': HandleSearch(Generation.Generation)
                case 'm': HandleSearch(Move.Move)
                case 'n': HandleSearch(Nature.Nature)
                case 'p': HandleSearch(Pokemon.Pokemon)
                # case 'q': HandleCacheTest()
                case 't': HandleSearch(Type.Type)
                # case '1':
                case '2':
                    ClearCaches()
                case '3':
                    ClearCaches(True)
                case '0':
                    Utils.ClearScreen()
                    exit(0)
                case _:
                    console.print("Not a valid key!")
                    printWelcome = False
                    pass

        except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the menu
            QuitGracefully()

    # TODO:
    #   Egg Groups
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
        # "[E]gg Groups",
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

def ClearCaches(doQuit=False):
    if os.path.exists(Utils.CACHE_DIR):
        shutil.rmtree(Utils.CACHE_DIR)

    for resource in RESOURCES.values():
        resource.NAME_TO_DATA_CACHE.clear()
        resource.ID_TO_NAME_CACHE.clear()

    if doQuit:
        exit(0)

def QuitGracefully():
    Utils.ClearScreen()
    SaveCaches()
    exit(0)

def HandleCacheTest():
    Utils.ClearCache()
    Utils.ClearScreen()
    console.rule("Cache Test", style='white')
    for i in track(range(1, 19), description='Fetching Type data...'):
        Type.Type.HandleSearch(str(i))
    for i in track(range(1, 10), description="Fetching Generation data..."):
        Generation.Generation.HandleSearch(str(i))
    for i in track(range(1, 251), description="Fetching Pokemon 1-250 data..."):
        Pokemon.Pokemon.HandleSearch(str(i))
    for i in track(range(1, 251), description="Fetching Move 1-250 data..."):
        Pokemon.Pokemon.HandleSearch(str(i))
    for i in track(range(251, 501), description="Fetching Pokemon 251-500 data..."):
        Pokemon.Pokemon.HandleSearch(str(i))
    for i in track(range(1, 251), description="Fetching Ability 1-250 data..."):
        Pokemon.Pokemon.HandleSearch(str(i))
    for i in track(range(501, 751), description="Fetching Pokemon 501-750 data..."):
        Pokemon.Pokemon.HandleSearch(str(i))
    SaveCaches()
    exit(0)

if __name__ == '__main__':
    main()
