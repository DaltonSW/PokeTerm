# Welcome to PokéTerm!
A terminal based PokéDex. It retrieves information from [PokeAPI](https://pokeapi.co/), and some very light web-scraping of [PokemonDB](https://pokemondb.net/) as a backup source. All data obtained is cached locally. The cache is stored in your home directory in a `.poketerm` folder 

Stylization is handled with [Rich](https://github.com/Textualize/rich). This program was tested with, and is intended to be used with, [Windows Terminal](https://apps.microsoft.com/detail/9N0DX20HK701?hl=en-US&gl=US). I have tested on WSL Ubuntu through Windows Terminal, and the default bash terminal on Mac, but I can't verify any other specific terminal programs on other systems.

### Go to the Releases tab and download the latest release. ###

It will likely be flagged as a virus on download and execution, but you can click "allow anyway". I used [PyInstaller](https://pyinstaller.org/en/stable/) to bundle the application, which is a common cause for false-positive results. 
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

<b>Recommended:</b> Put this in a virtual environment

Create a folder for the project. Right-click inside and click `Open in Terminal`.
```ps
git clone 'https://github.com/DaltonSW/PokeTerm.git' # Download the codebase to the folder
python -m venv .venv # Create a Python virtual environment named '.venv'
```
</details>
