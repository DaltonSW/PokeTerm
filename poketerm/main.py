from sys import exit
from readchar import readkey, key as keys
from rich import box
from rich.table import Table

from poketerm.utils import testing
import poketerm.utils.updater as updater

from poketerm.console import console
from poketerm.resources import move, ability, type, pokemon, species
from poketerm.resources import version, generation
from poketerm.resources import version_group, nature, egg_group
from poketerm.utils.visual import print_resource_data, clear_screen, print_welcome

from poketerm.utils.searching import SearchManager
from poketerm.utils.caching import CacheManager

# TODO:
#   Location
#   Item
#   Game/Version
#   PokeBalls
#   Catch Rate Calculator


# region Main Util Functions
def startup():
    CacheManager.load_mappings()


def shutdown():
    CacheManager.save_mappings()
    exit(0)


def handle_cache_test():
    CacheManager.clear_mappings()
    testing.handle_cache_test()
    shutdown()


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
    # "Version": version.Version,
    # "Species": species.Species,
    # "VersionGroup": version_group.VersionGroup,
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
    "a": ability.Ability,
    "e": egg_group.EggGroup,
    "g": generation.Generation,
    "m": move.Move,
    "n": nature.Nature,
    "p": pokemon.Pokemon,
    "t": type.Type,
}

ADMIN_DISPATCH = {
    "q": handle_cache_test,
    "2": CacheManager.clear_mappings,
    "0": shutdown,
}


def main():
    startup()

    SearchManager.load_valid_names([RESOURCES[name] for name in RESOURCES.keys()])

    if updater.check_for_update():
        shutdown()

    while True:
        try:
            clear_screen(True)
            print_welcome()
            print_choices()
            key = readkey()
            if key == keys.ENTER:
                shutdown()

            console.clear()
            handle_dispatch(key)

        except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the menu
            shutdown()


def handle_dispatch(key):
    if key in ADMIN_DISPATCH:
        ADMIN_DISPATCH[key]()
    if key not in SEARCH_DISPATCH:
        console.print("Not a valid key!")
        return

    search_resource = SEARCH_DISPATCH[key]

    # Now we know we're trying to search on something
    resource = SearchManager.handle_search_and_cast(search_resource)

    if resource is None:
        return

    CacheManager.cache_resource(resource)

    print_resource_data(resource)

    return


def print_choices():
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


if __name__ == "__main__":
    main()
