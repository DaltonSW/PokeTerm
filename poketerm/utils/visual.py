import os
from poketerm.console import console
from readchar import readkey, key as keys
from poketerm.utils.general import IsWindowsOS


def PrintData(data) -> None:
    while True:
        ClearScreen()
        data.print_data()
        print()
        console.rule("Press [Enter] to return to the menu.", characters=" ")
        key = readkey()
        if key == keys.ENTER:
            return
        data.ToggleFlag(key)


def ClearScreen(keepHistory=False) -> None:
    if keepHistory:
        console.clear()
        return

    os.system("cls" if IsWindowsOS() else "clear")
