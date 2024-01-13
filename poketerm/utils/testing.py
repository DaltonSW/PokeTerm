from concurrent.futures import ThreadPoolExecutor
from poketerm.console import console

from poketerm.resources import pokemon, generation, move, ability, type, nature
from poketerm.resources import item, location, machine, pokedex, region

from rich.progress import Progress, BarColumn, MofNCompleteColumn, TimeElapsedColumn

from readchar import readchar

GEN_ONE_POKES = 151
GEN_TWO_POKES = 251
GEN_THREE_POKES = 386
GEN_FOUR_POKES = 493
GEN_FIVE_POKES = 650
GEN_SIX_POKES = 721
GEN_SEVEN_POKES = 809
GEN_EIGHT_POKES = 898
GEN_NINE_POKES = 1025

GENERATION_COUNT = 9
REGION_COUNT = 10
TYPE_COUNT = 18
NATURE_COUNT = 24
POKEDEX_COUNT = 33  # Includes up to Blueberry Dex
ABILITY_COUNT = 307
LOCATION_COUNT = 867  # This doesn't include any ScVi DLC
MOVE_COUNT = 919
POKEMON_COUNT = 1025
MACHINE_COUNT = 1688  # Unsure if this includes ANYTHING from ScVi
ITEM_COUNT = 2159

POKE_COUNTS = [
    0,
    GEN_ONE_POKES,
    GEN_TWO_POKES,
    GEN_THREE_POKES,
    GEN_FOUR_POKES,
    GEN_FIVE_POKES,
    GEN_SIX_POKES,
    GEN_SEVEN_POKES,
    GEN_EIGHT_POKES,
    GEN_NINE_POKES,
]

progress = Progress(
    "{task.description}", BarColumn(), MofNCompleteColumn(), TimeElapsedColumn()
)


def HandleTestRange(resource, taskID, count):
    for i in range(1, count + 1):
        HandleSingleTest(resource, taskID, i)


def HandleSingleTest(resource, taskID, query):
    resource.HandleSearch(query)
    progress.update(taskID, advance=1)


def HandleCacheTest():
    console.clear()
    console.rule("Cache Test", style="white")

    genID = progress.add_task("Loading Generation Information", total=GENERATION_COUNT)
    regionID = progress.add_task("Loading Region Information", total=REGION_COUNT)
    typeID = progress.add_task("Loading Type Information", total=TYPE_COUNT)
    natureID = progress.add_task("Loading Nature Information", total=NATURE_COUNT)
    pokedexID = progress.add_task("Loading Pokedex Information", total=POKEDEX_COUNT)
    abilityID = progress.add_task("Loading Ability Information", total=ABILITY_COUNT)
    locationID = progress.add_task("Loading Location Information", total=LOCATION_COUNT)
    moveID = progress.add_task("Loading Move Information", total=MOVE_COUNT)
    pokeID = progress.add_task("Loading Pokemon Information", total=POKEMON_COUNT)
    machineID = progress.add_task("Loading Machine Information", total=MACHINE_COUNT)
    itemID = progress.add_task("Loading Item Information", total=ITEM_COUNT)

    with progress:
        with ThreadPoolExecutor() as executor:
            executor.submit(HandleTestRange, item.Item, itemID, ITEM_COUNT)
            executor.submit(HandleTestRange, machine.Machine, machineID, MACHINE_COUNT)
            executor.submit(HandleTestRange, pokemon.Pokemon, pokeID, POKEMON_COUNT)
            executor.submit(HandleTestRange, move.Move, moveID, MOVE_COUNT)
            executor.submit(
                HandleTestRange, location.Location, locationID, LOCATION_COUNT
            )
            executor.submit(HandleTestRange, pokedex.Pokedex, pokedexID, POKEDEX_COUNT)
            executor.submit(HandleTestRange, ability.Ability, abilityID, ABILITY_COUNT)
            executor.submit(HandleTestRange, nature.Nature, natureID, NATURE_COUNT)
            executor.submit(HandleTestRange, type.Type, typeID, TYPE_COUNT)
            executor.submit(HandleTestRange, region.Region, regionID, REGION_COUNT)
            executor.submit(
                HandleTestRange, generation.Generation, genID, GENERATION_COUNT
            )
    _ = readchar()


if __name__ == "__main__":
    HandleCacheTest()
