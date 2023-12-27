# Welcome to PokéTerm!
A (presently) Windows-only, terminal based Pokédex. It retrieves information from [PokeAPI](https://pokeapi.co/), and some very light web-scraping of [PokemonDB](https://pokemondb.net/) as a backup source. All data obtained is cached locally. The program may be run fully portably, but the generated `cache` folder needs to be in the same location as the main EXE to be able to access it. 

Stylization is handled with [Rich](https://github.com/Textualize/rich). This program was tested with, and is intended to be used with, [Windows Terminal](https://apps.microsoft.com/detail/9N0DX20HK701?hl=en-US&gl=US). 

### Go to the Releases tab and download the EXE of the newest release. ###

It will likely be flagged as a virus on download and execution, but you can click "allow anyway". I used [PyInstaller](https://pyinstaller.org/en/stable/) to bundle the EXE, which is a common cause for false-positive results. 
There's nothing I can do about that at this time, but I've submitted the program to various organizations for analysis, so it will be properly flagged in the future. Code signature certificates are very pricey, so that's not viable for me right now.

You can view the results of the VirusTotal scan here: [Link](https://www.virustotal.com/gui/file/9c894b40c4940ce9791655c3bb1087b2b18f88260f88431526a5562e37076297)

Please reach out with any questions or issues. You can leave an issue on the repo, email me at [feedback@dalton.dog](mailto:feedback@dalton.dog), or message me on Discord `@DaltonSW`

<details>
<summary>Upcoming Features!</summary>
 <ul>
  <li>Configuration Options</li>
   <ul>
    <li>Colorblind Mode</li>
    <li>Background caching of information</li>
    <li>Limiting information by generations</li>
   </ul>
  <li>Prettier and Improved Layouts</li>
  <li>More Accurate and Detailed Information</li>
  <li>More Things to Search On</li>
  <li>Fuzzy Searching</li>
  <li>Rendering "Links" to Other Pages (Ex: Jump to "Grass" type screen directly from "Bulbasaur" page)</li>
  <li>Calculators</li>
  <li>Plenty of other stuff that I think of as the project continues!</li>
 </ul>
</details>

![Homescreen of the terminal application, displaying the title and some menu choices.](https://i.imgur.com/wRvhXIn.png)

![Example of searching on Type, with "Fire" used as the example search.](https://i.imgur.com/PIc3WAq.png)

![Example of searching on Pokemon, with "Dratini" used as the example search.](https://i.imgur.com/BpulMLS.png)

<details>
<summary>Manual Installation Instructions</summary>
<b>Requirement:</b> You must have Python installed. I don't presently know what version range works, but I've been developing on 3.11.  

<b>Recommended:</b> Have some sort of Git client installed (either Git Bash or GitHub Desktop) to clone the repo. While you can download the source code as a ZIP and run it, you won't be able to easily obtain any updates I'll be making.

<b>Recommended:</b> Put this in a virtual environment. If you use the environment name in the code block below, you can simply run the included PowerShell script to launch the program

Create a folder for the project. Right-click inside and click `Open in Terminal`.
```ps
git clone 'https://github.com/DaltonSW/PokeTerm.git' # Download the codebase to the folder
python -m venv .venv # Create a Python virtual environment named '.venv'
```
If you created the virtual environment with the name `.venv`, then you can just run `.\poketerm.ps1` to start the program. If you named it something else, you'll need to edit the `.ps1` file to change the directory to match your environment's name.
 
 Going forward, you can use that `.ps1` script to run the program from here. You should be able to create a shortcut to it and put it elsewhere. The script will automatically pull in any updates automatically, and install any newly required Python modules.

</details>
