import os
import shutil

from sys import exit
from readchar import readkey, key as keys
from rich import box
from rich.table import Table

from poketerm import utils
import poketerm.updater as updater

from poketerm.console import console
from poketerm.config import Config
from poketerm.resources import move, ability, type, pokemon, species
from poketerm.resources import version, generation
from poketerm.resources import version_group, nature, egg_group


# region Main Util Functions
def SaveCaches():
    if not os.path.exists(utils.CACHE_DIR):
        os.makedirs(utils.CACHE_DIR)
    for resource in RESOURCES.values():
        resource.SaveCache()

    Config.SaveCache()


def LoadCaches():
    for resource in RESOURCES.values():
        resource.LoadCache()

    Config.LoadCache()
    console.clear()


def ClearCaches(doQuit=False):
    if os.path.exists(utils.CACHE_DIR):
        shutil.rmtree(utils.CACHE_DIR)

    for resource in RESOURCES.values():
        resource.NAME_TO_DATA_CACHE.clear()
        resource.ID_TO_NAME_CACHE.clear()

    if doQuit:
        exit(0)


def HandleSearch(resource):
    query = input(f"{resource.ENDPOINT.title()} Name or ID: ").lower()
    if query == "":
        return

    with console.status(f"Querying for {resource.ENDPOINT.title()}..."):
        result = resource.HandleSearch(query)
    if result is not None:
        utils.PrintData(result)
    return


def QuitGracefully():
    SaveCaches()
    console.clear()
    exit(0)


# endregion

BASE_URL = "https://pokeapi.co/api/v2/"
RESOURCES = {
    "ability": ability.Ability,
    # 'Berry': Berry.Berry,
    "EggGroup": egg_group.EggGroup,
    "Generation": generation.Generation,
    # 'Item': Item.Item,
    # 'Location': Location.Location,
    "Move": move.Move,
    "Nature": nature.Nature,
    "Pokemon": pokemon.Pokemon,
    "Type": type.Type,
    "Version": version.Version,
    "Species": species.Species,
    "VersionGroup": version_group.VersionGroup,
}

SEARCH_OPTIONS = [
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
    "[T]ype",
]

ADMIN_OPTIONS = [
    # "[1] Options",
    "[2] Clear Cache",
    "[3] Clear Cache & Quit",
    "[0] Quit Without Saving",
    # "[Enter] Save & Quit"
]

SEARCH_DISPATCH = {
    "e": lambda: HandleSearch(egg_group.EggGroup),
    "g": lambda: HandleSearch(generation.Generation),
    "m": lambda: HandleSearch(move.Move),
    "n": lambda: HandleSearch(nature.Nature),
    "p": lambda: HandleSearch(pokemon.Pokemon),
    "t": lambda: HandleSearch(type.Type),
}

ADMIN_DISPATCH = {"2": ClearCaches, "3": lambda: ClearCaches(True), "0": QuitGracefully}


def main():
    LoadCaches()

    if updater.CheckForUpdate():
        SaveCaches()
        exit(0)

    while True:
        try:
            utils.ClearScreen(True)
            PrintWelcome()
            PrintChoices()
            key = readkey()
            if key == keys.ENTER:
                QuitGracefully()

            console.clear()

            if key in SEARCH_DISPATCH:
                SEARCH_DISPATCH[key]()
            elif key in ADMIN_DISPATCH:
                ADMIN_DISPATCH[key]()
            else:
                console.print("Not a valid key!")

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
    console.rule(
        "[bold white]Press a bracketed letter to search on that topic.", characters=" "
    )
    console.rule("[bold white]Press Enter to save caches and exit.", characters=" ")

    overallTable = Table(show_header=False, box=box.SIMPLE)

    searchTable, adminTable = Table(show_header=False, box=box.SIMPLE), Table(
        show_header=False, box=box.SIMPLE
    )

    for option in SEARCH_OPTIONS:
        searchTable.add_row(f"[bold]{option}[/]")

    for option in ADMIN_OPTIONS:
        adminTable.add_row(f"[bold]{option}[/]")

    overallTable.add_row(searchTable, adminTable)

    console.print(overallTable, justify="center")
    console.rule("[bold white]\[Enter] Save & Quit[/]", characters=" ")


def PrintWelcome():
    console.rule("[red]     #########    [/]", characters=" ")
    console.rule("[red]   #############  [/]", characters=" ")
    console.rule("[red]  ############### [/]", characters=" ")
    console.rule("[red] #####       #####[/]", characters=" ")
    console.rule("[white]        ###       [/]", characters=" ")
    console.rule("[white]        ###       [/]", characters=" ")
    console.rule("[white] #####       #####[/]", characters=" ")
    console.rule("[white]  ############### [/]", characters=" ")
    console.rule("[white]   #############  [/]", characters=" ")
    console.rule("[white]     #########    [/]", characters=" ")
    print()
    console.rule(f"[bold white]Welcome to [red]Poké[/]Term!", style="white")
    console.rule(f"Cache is stored at ~{os.sep}.poketerm", characters=" ")


if __name__ == "__main__":
    main()
