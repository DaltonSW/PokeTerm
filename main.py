import os
import shutil
from InquirerPy import inquirer
from PokeWrapper import PokeWrapper
import Utils
from console import console

# TODO: Set up "configuration" to collapse/expand certain sections

# TODO: Make it pretty AND interactive with some TUI framework
# TODO: Once you've got basic information searching working, set up links between them
# TODO: Make links clickable

def main():
    PokeWrapper.LoadCaches()
    Utils.ClearScreen()
    prompt = "What to search for?"
    options = [
        'Pokemon',
        'Ability',
        # 'Type',
        'Move',
        # 'Berry',
        # 'Location',
        # 'Item',
        'Version',
        'Generation',
        'Cache Test',
        'Clear Cache',
        'Clear & Quit',
        'Quit'
    ]
    choice = ''

    while True:
        console.print(f"Welcome to [bold][red]Poké[/][white]Term![/][/]")
        try:
            choice = inquirer.select(
                message=prompt,
                choices=options
            ).execute()

        except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the menu
            QuitGracefully()

        if choice == 'Quit' or choice == '':
            QuitGracefully()

        elif choice == 'Clear Cache' or choice == 'Clear & Quit':
            if os.path.exists('./cache'):
                shutil.rmtree('./cache')
            Utils.ClearScreen()
            if choice == 'Clear & Quit':
                quit(0)

        elif choice == 'Cache Test':
            if os.path.exists('./cache'):
                shutil.rmtree('./cache')
            PokeWrapper.HandleCacheTest()
            QuitGracefully()

        else:
            try:
                PokeWrapper.HandleSearch(choice)
                Utils.ClearScreen()
            except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the info screen
                QuitGracefully()

def QuitGracefully():
    Utils.ClearScreen()
    PokeWrapper.SaveCaches()
    quit(0)

if __name__ == '__main__':
    main()
