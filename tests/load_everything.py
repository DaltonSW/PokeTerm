from poketerm.main import ClearCaches, SaveCaches
from concurrent.futures import ThreadPoolExecutor
from poketerm.console import console

from poketerm.resources import pokemon, generation, move, ability, type, nature

from rich.progress import Progress, BarColumn, MofNCompleteColumn

GEN_ONE_POKES = 151
GEN_TWO_POKES = 251
GEN_THREE_POKES = 386
GEN_FOUR_POKES = 493
GEN_FIVE_POKES = 650
GEN_SIX_POKES = 721
GEN_SEVEN_POKES = 809
GEN_EIGHT_POKES = 898
GEN_NINE_POKES = 1025
ABILITY_COUNT = 307
MOVE_COUNT = 919
GENERATION_COUNT = 9
NATURE_COUNT = 24
TYPE_COUNT = 18

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
    "{task.description}",
    BarColumn(),
    MofNCompleteColumn(),
)


def HandleSingleTest(resource, taskID, query):
    resource.HandleSearch(query)
    progress.update(taskID, advance=1)


def HandleCacheTest():
    ClearCaches()
    console.clear()
    console.rule("Cache Test", style="white")

    genID = progress.add_task("Loading Generation Information", total=GENERATION_COUNT)
    typeID = progress.add_task("Loading Type Information", total=TYPE_COUNT)
    natureID = progress.add_task("Loading Nature Information", total=NATURE_COUNT)
    abilityID = progress.add_task("Loading Ability Information", total=ABILITY_COUNT)
    moveID = progress.add_task("Loading Move Information", total=MOVE_COUNT)
    pokeID = progress.add_task("Loading Pokemon Information", total=GEN_NINE_POKES)

    with progress:
        with ThreadPoolExecutor() as executor:
            for i in range(1, GEN_NINE_POKES + 1):
                executor.submit(HandleSingleTest, pokemon.Pokemon, pokeID, i)

            for i in range(1, GENERATION_COUNT + 1):
                executor.submit(HandleSingleTest, generation.Generation, genID, i)

            for i in range(1, TYPE_COUNT + 1):
                executor.submit(HandleSingleTest, type.Type, typeID, i)

            for i in range(1, MOVE_COUNT + 1):
                executor.submit(HandleSingleTest, move.Move, moveID, i)

            for i in range(1, NATURE_COUNT + 1):
                executor.submit(HandleSingleTest, nature.Nature, natureID, i)

            for i in range(1, ABILITY_COUNT + 1):
                executor.submit(HandleSingleTest, ability.Ability, abilityID, i)
    SaveCaches()
    exit(0)
