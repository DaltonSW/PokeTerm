import os
from poketerm.console import console
from readchar import readkey, key as keys
from poketerm.utils.general import is_windows


def print_resource_data(resource) -> None:
    while True:
        clear_screen()
        resource.print_data()
        print()
        console.rule("Press [Enter] to return to the menu.", characters=" ")
        key = readkey()
        if key == keys.ENTER:
            return
        resource.toggle_flag(key)


def clear_screen(keepHistory=False) -> None:
    if keepHistory:
        console.clear()
        return

    os.system("cls" if is_windows() else "clear")


def print_welcome():
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
    console.rule(f"Cache is stored in ~{os.sep}.poketerm", characters=" ")
