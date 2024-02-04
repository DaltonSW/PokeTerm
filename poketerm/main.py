import os

from sys import exit
from readchar import readkey, key as keys
from rich import box
from rich.table import Table

from poketerm.utils import testing
import poketerm.utils.updater as updater

from poketerm.console import console
from poketerm.config import Config
from poketerm.resources import move, ability, type, pokemon, species
from poketerm.resources import version, generation
from poketerm.resources import version_group, nature, egg_group
from poketerm.utils.visual import PrintData, ClearScreen

from poketerm.utils.searching import SearchManager
from poketerm.utils.caching import CacheManager

# TODO:
#   Location
#   Item
#   Game/Version
#   PokeBalls
#   Catch Rate Calculator


# region Main Util Functions
def quit_gracefully():
    CacheManager.save_caches()
    console.clear()
    exit(0)


def handle_cache_test():
    CacheManager.clear_caches()
    testing.HandleCacheTest()
    CacheManager.save_caches()
    exit(0)


# endregion

RESOURCES = {
    "Ability": ability.Ability,
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
    "[A]bility",
    # "[B]erry",
    "[C]alculators",
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
    "[0] Quit Without Saving",
]

SEARCH_DISPATCH = {
    "a": ability.Ability.ENDPOINT,
    "e": egg_group.EggGroup.ENDPOINT,
    "g": generation.Generation.ENDPOINT,
    "m": move.Move.ENDPOINT,
    "n": nature.Nature.ENDPOINT,
    "p": pokemon.Pokemon.ENDPOINT,
    "t": type.Type.ENDPOINT,
}

ADMIN_DISPATCH = {
    "q": handle_cache_test,
    "2": CacheManager.clear_caches,
    "0": quit_gracefully,
}


def main():
    CacheManager.load_caches()

    if updater.CheckForUpdate():
        CacheManager.save_caches()
        exit(0)

    while True:
        try:
            ClearScreen(True)
            PrintWelcome()
            PrintChoices()
            key = readkey()
            if key == keys.ENTER:
                quit_gracefully()

            console.clear()
            handle_dispatch(key)

        except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the menu
            quit_gracefully()


def handle_dispatch(key):
    if key in ADMIN_DISPATCH:
        ADMIN_DISPATCH[key]()
    if key not in SEARCH_DISPATCH:
        console.print("Not a valid key!")
        return

    # Now we know we're trying to search on something
    data = SearchManager.handle_search(SEARCH_DISPATCH[key])
    print(data)

    return


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
