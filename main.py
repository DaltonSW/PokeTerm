import os
from InquirerPy import inquirer
from PokeWrapper import PokeWrapper

def main():
    PokeWrapper.LoadCaches()
    os.system('cls' if os.name == 'nt' else 'clear')
    prompt = "What to search for?"
    options = [
        # 'Pokemon',
        # 'Ability',
        # 'Type',
        'Move',
        # 'Berry',
        # 'Location',
        # 'Item',
        # 'Version',
        # 'New Option',
        'Quit'
    ]
    choice = ''

    while True:
        try:
            choice = inquirer.select(
                message=prompt,
                choices=options
            ).execute()

        except KeyboardInterrupt:
            QuitGracefully()

        if choice == 'Quit' or choice == '':
            QuitGracefully()
        PokeWrapper.HandleSearch(choice)

def QuitGracefully():
    os.system('cls' if os.name == 'nt' else 'clear')
    PokeWrapper.SaveCaches()
    quit(0)

if __name__ == '__main__':
    main()
