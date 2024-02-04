import os
from poketerm.console import console
from readchar import readkey, key as keys
from poketerm.utils.general import IsWindowsOS


def print_resource_data(resource) -> None:
    while True:
        ClearScreen()
        resource.print_data()
        print()
        console.rule("Press [Enter] to return to the menu.", characters=" ")
        key = readkey()
        if key == keys.ENTER:
            return
        resource.ToggleFlag(key)


def ClearScreen(keepHistory=False) -> None:
    if keepHistory:
        console.clear()
        return

    os.system("cls" if IsWindowsOS() else "clear")


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
    console.rule(f"Cache is stored at ~{os.sep}.poketerm", characters=" ")
