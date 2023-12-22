# Welcome to PokéTerm!
A (presently) Windows-only, terminal based PokeDex. It retrieves information from [PokeAPI](https://pokeapi.co/), and some very light web-scraping of [PokemonDB](https://pokemondb.net/). All data obtained is cached locally, and any web-scraping done is has a manual delay added, so as to not pull from any servers more than a human realistically would be able to. 

Stylization is handled with [Rich](https://github.com/Textualize/rich). This program is intended to be used with [Windows Terminal](https://apps.microsoft.com/detail/9N0DX20HK701?hl=en-US&gl=US).

## Installation Instructions
<b>Requirement:</b> You must have Python installed. I don't presently know what version range works, but I've been developing on 3.11.  

<b>Recommended:</b> Have some sort of Git client installed (either Git Bash or Github Desktop) to clone the repo. While you can download the source code as a ZIP and run it, you won't be able to easily obtain any updates I'll be making.

<b>Recommended:</b> Put this in a virtual environment. If you use the environment name in the code block below, you can simply run the included PowerShell script to launch the program

Create a folder for the project. Right-click inside and click `Open in Terminal`.
```ps
git clone 'https://github.com/DaltonSW/PokeTerm.git' # Download the codebase to the folder
python -m venv .venv # Create a Python virtual environment named '.venv'
```
If you created the virtual environment with the name `.venv`, then you can just run `.\poketerm.ps1` to start the program. If you named it something else, you'll need to edit the `.ps1` file to change the directory to match your environment's name.
 
 Going forward, you can use that `.ps1` script to run the program from here. You should be able to create a shortcut to it and put it elsewhere. The script will automatically pull in any updates automatically, and install any newly required Python modules.
