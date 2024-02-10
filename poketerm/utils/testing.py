import asyncio
from concurrent.futures import ThreadPoolExecutor

import aiohttp

from poketerm.console import console

from poketerm.resources import (
    pokemon,
    generation,
    move,
    ability,
    type,
    nature,
    egg_group,
    item,
    location,
    machine,
    pokedex,
    region,
)

from poketerm.utils.searching import SearchManager, obtain_data_async
from poketerm.utils.caching import CacheManager

from rich.progress import Progress, BarColumn, MofNCompleteColumn, TimeElapsedColumn

from readchar import readchar

TEST_RUNNING = False

TESTABLE_RESOURCES = {
    "Generation": generation.Generation,  # 9
    "Egg Group": egg_group.EggGroup,  # 15
    "Type": type.Type,  # 18
    "Nature": nature.Nature,  # 24
    "Ability": ability.Ability,  # 307
    "Move": move.Move,  # 919
    "Pokemon": pokemon.Pokemon,  # 1025
    # "Item": item.Item,  # 2159
    # "Machine": machine.Machine,  # 1688S
    # "Location": location.Location,  # 867
    # "Pokedex": pokedex.Pokedex,  # 33
    # "Region": region.Region,  # 10
}

progress = Progress(
    "{task.description}", BarColumn(), MofNCompleteColumn(), TimeElapsedColumn()
)


def handle_resource_test(resource, taskID):
    for i in range(1, resource.MAX_COUNT + 1):
        handle_single_query(resource, taskID, i)


def handle_single_query(resource, taskID, query):
    res = SearchManager.handle_search_and_cast(resource, query)
    SearchManager.update_valid_names(res)
    progress.update(taskID, advance=1)


async def handle_resource_async(resource, taskID):
    async with aiohttp.ClientSession() as session:
        for i in range(1, resource.MAX_COUNT + 1):
            await handle_query_async(resource, taskID, i, session)


async def handle_query_async(resource, taskID, query, session):
    data = await obtain_data_async(resource.ENDPOINT, query, session)
    res = resource(data)
    SearchManager.update_valid_names(res)
    CacheManager.cache_resource(res)
    progress.update(taskID, advance=1)


def handle_cache_test():
    global TEST_RUNNING
    TEST_RUNNING = False
    console.clear()
    console.rule("Cache Test", style="white")

    with progress:
        with ThreadPoolExecutor() as executor:
            for resource in TESTABLE_RESOURCES.values():
                taskID = progress.add_task(
                    f"Loading {resource.ENDPOINT} info...", total=resource.MAX_COUNT
                )
                executor.submit(handle_resource_test, resource, taskID)
    _ = readchar()

    CacheManager.save_mappings()
    SearchManager.save_valid_names()


async def handle_test_async():
    global TEST_RUNNING
    TEST_RUNNING = False
    console.clear()
    console.rule("Async Cache Test", style="white")

    with progress:
        tasks = []
        for resource in TESTABLE_RESOURCES.values():
            taskID = progress.add_task(
                f"Loading {resource.ENDPOINT} info...", total=resource.MAX_COUNT
            )
            tasks.append(handle_resource_async(resource, taskID))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    # handle_cache_test()
    asyncio.run(handle_test_async())
