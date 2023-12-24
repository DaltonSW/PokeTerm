import os
import shutil
from InquirerPy import inquirer
from PokeWrapper import PokeWrapper
import Utils
from console import console

# Known Pokemon Edge Cases:
#   Searching Pokemon for "Minior"
#   Printing out Eevee's evolutions

# TODO:
#   Overhaul the choice system to make it character based like the rest of the screens
#   Set up "configuration" to collapse/expand certain sections
#   Once you've got basic information searching working, set up links between them
#   Make links "clickable"
#       Ask Discord if I can have clicking a link redirect to a funcion instead?
#       First just look into the code and see if it can be overridden or something?

def main():
    PokeWrapper.LoadCaches()
    Utils.ClearScreen()
    # TODO:
    #   Egg Groups
    #   Location
    #   Item
    #   Game/Version
    #   PokeBalls
    #   Catch Rate Calculator
    prompt = "What to search for?"
    options = [
        'Pokemon',
        # 'Ability',
        'Type',
        'Move',
        # 'Berry',
        # 'Location',
        # 'Item',
        'Version',
        'Generation',
        'Cache Test',
        'Clear Cache & Quit',
        'Quit'
    ]
    choice = ''

    while True:
        PrintWelcome()
        try:
            choice = inquirer.select(
                message=prompt,
                choices=options
            ).execute()

        except KeyboardInterrupt:  # This handles Ctrl+C'ing out of the menu
            QuitGracefully()

        if choice == 'Quit' or choice == '':
            QuitGracefully()

        elif choice == 'Clear Cache & Quit':
            if os.path.exists('./cache'):
                shutil.rmtree('./cache')
            Utils.ClearScreen()
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

def PrintWelcome():
    console.rule('[red]     #########    [/]', characters=' ')
    console.rule('[red]   #############  [/]', characters=' ')
    console.rule('[red]  ############### [/]', characters=' ')
    console.rule('[red] #####       #####[/]', characters=' ')
    console.rule('[white]        ###       [/]', characters=' ')
    console.rule('[white]        ###       [/]', characters=' ')
    console.rule('[white] #####       #####[/]', characters=' ')
    console.rule('[white]  ############### [/]', characters=' ')
    console.rule('[white]   #############  [/]', characters=' ')
    console.rule('[white]     #########    [/]', characters=' ')
    print()
    console.rule(f"[bold white]Welcome to [red]Poké[/]Term!", style='white')


def QuitGracefully():
    Utils.ClearScreen()
    PokeWrapper.SaveCaches()
    quit(0)

if __name__ == '__main__':
    main()
