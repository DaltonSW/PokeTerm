from main import ClearCaches, SaveCaches
from concurrent.futures import ThreadPoolExecutor
from console import console

from rich.progress import Progress, BarColumn, MofNCompleteColumn

from resources import type, generation, pokemon, ability, move, nature

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


def HandleSingleTest(resource, taskID, rangeEnd: int, rangeStart=1):
    for i in range(rangeStart, rangeEnd + 1):
        resource.HandleSearch(i)
        progress.update(taskID, advance=1)


def HandleCacheTest():
    ClearCaches()
    console.clear()
    console.rule("Cache Test", style="white")

    genID = progress.add_task("Loading Generation Information", total=GENERATION_COUNT)
    typeID = progress.add_task("Loading Type Information", total=TYPE_COUNT)
    natureID = progress.add_task("Loading Nature Information", total=NATURE_COUNT)
    abilityID = progress.add_task("Loading Ability Information", total=ABILITY_COUNT)
    moveOneID = progress.add_task(
        "Loading First Half of Move Information", total=MOVE_COUNT // 2
    )
    moveTwoID = progress.add_task(
        "Loading Second Half of Move Information", total=MOVE_COUNT - (MOVE_COUNT // 2)
    )

    with progress:
        with ThreadPoolExecutor() as executor:
            for i in range(1, 10):
                pokeID = progress.add_task(
                    f"Loading Pokemon from Gen {i}",
                    total=POKE_COUNTS[i] - POKE_COUNTS[i - 1],
                )
                executor.submit(
                    HandleSingleTest,
                    Pokemon.Pokemon,
                    pokeID,
                    POKE_COUNTS[i],
                    POKE_COUNTS[i - 1] + 1,
                )
            executor.submit(
                HandleSingleTest, Ability.Ability, abilityID, ABILITY_COUNT, 1
            )
            executor.submit(HandleSingleTest, Move.Move, moveOneID, MOVE_COUNT // 2, 1)
            executor.submit(
                HandleSingleTest,
                Move.Move,
                moveTwoID,
                MOVE_COUNT,
                (MOVE_COUNT // 2) + 1,
            )
            executor.submit(
                HandleSingleTest, Generation.Generation, genID, GENERATION_COUNT, 1
            )
            executor.submit(HandleSingleTest, Nature.Nature, natureID, NATURE_COUNT, 1)
            executor.submit(HandleSingleTest, Type.Type, typeID, TYPE_COUNT, 1)
    SaveCaches()
    exit(0)
