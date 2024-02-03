from concurrent.futures import ThreadPoolExecutor
from poketerm.console import console

from poketerm.resources import pokemon, generation, move, ability, type, nature
from poketerm.resources import item, location, machine, pokedex, region

from rich.progress import Progress, BarColumn, MofNCompleteColumn, TimeElapsedColumn

from readchar import readchar

TESTABLE_RESOURCES = {
    "Generation": generation.Generation,  # 9
    "Region": region.Region,  # 10
    "Type": type.Type,  # 18
    "Nature": nature.Nature,  # 24
    "Pokedex": pokedex.Pokedex,  # 33
    "Ability": ability.Ability,  # 307
    # "Location": location.Location,  # 867
    # "Move": move.Move,  # 919
    # "Pokemon": pokemon.Pokemon,  # 1025
    # "Machine": machine.Machine,  # 1688
    # "Item": item.Item,  # 2159
}

progress = Progress(
    "{task.description}", BarColumn(), MofNCompleteColumn(), TimeElapsedColumn()
)


def HandleResourceTest(resource, taskID):
    for i in range(1, resource.MAX_COUNT + 1):
        HandleSingleQuery(resource, taskID, i)


def HandleSingleQuery(resource, taskID, query):
    resource.HandleSearch(query)
    progress.update(taskID, advance=1)


def HandleCacheTest():
    console.clear()
    console.rule("Cache Test", style="white")

    with progress:
        with ThreadPoolExecutor() as executor:
            for resource in TESTABLE_RESOURCES.values():
                taskID = progress.add_task(
                    f"Loading {resource.ENDPOINT} info...", total=resource.MAX_COUNT
                )
                executor.submit(HandleResourceTest, resource, taskID)
    _ = readchar()


if __name__ == "__main__":
    HandleCacheTest()
