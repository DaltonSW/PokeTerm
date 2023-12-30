import subprocess
import os

import Utils
from Config import APP_VERSION
import requests

from readchar import readkey, key as keys

from console import console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)


def CheckForUpdate() -> bool:
    # Check for updaters and delete them if they exist
    if os.path.exists('update_poketerm.bat'):
        os.remove('update_poketerm.bat')

    if os.path.exists('update_poketerm.sh'):
        os.remove('update_poketerm.sh')

    # Check GitHub for if "latest" is not current version
    req = requests.get('https://github.com/DaltonSW/PokeTerm/releases/latest')
    if req.status_code != 200:
        console.print("Couldn't connect to repository. Returning.")
        return False

    try:
        newVersion = req.url.split('/')[-1]
        major, minor, patch = newVersion.split('.')
    except IndexError:
        console.print("Invalid URL loaded. Returning.")
        return False

    appMajor, appMinor, appPatch = APP_VERSION.split('.')
    if int(appMajor) < int(major):
        return PromptForUpdate(newVersion)
    elif int(appMinor) < int(minor):
        return PromptForUpdate(newVersion)
    elif int(appPatch) < int(patch):
        return PromptForUpdate(newVersion)

    return False

def PromptForUpdate(newVersion) -> bool:
    console.print("New version found! Press \[Enter] to download.")
    key = readkey()
    if key == keys.ENTER:
        return DownloadUpdate(newVersion)
    return False

# Rich Progress bar implementation derived from Will McGugan's example
# https://github.com/Textualize/rich/blob/master/examples/downloader.py#L47
def DownloadUpdate(version: str) -> bool:
    baseURL = f'https://github.com/DaltonSW/PokeTerm/releases/download/{version}/'
    fileName = 'PokeTerm_' + 'Windows.exe' if Utils.IsWindowsOS() else 'PokeTerm_' + 'Linux'
    downloadURL = baseURL + fileName

    chunkSize = 32768

    with requests.get(downloadURL, stream=True) as downloadRequest:
        if downloadRequest.status_code != 200:
            console.print("Couldn't download PokeTerm. Returning")
            return False

        with progress:
            downloadTaskID = progress.add_task(f"Downloading PokeTerm v{version}", total=int(downloadRequest.headers.get('Content-Length', 0)), filename=fileName)
            with open(f"./{fileName}", 'wb') as newFile:
                for data in downloadRequest.iter_content(chunk_size=chunkSize):
                    newFile.write(data)
                    progress.update(downloadTaskID, advance=chunkSize)

    console.print("New version downloaded! Press \[Enter] to restart the program.")
    key = readkey()
    if key == keys.ENTER:
        return CreateUpdateScriptAndUpdate()
    return False

def CreateUpdateScriptAndUpdate():
    if Utils.IsWindowsOS():
        with open('.\\update_poketerm.bat', 'w') as file:
            file.write(WINDOWS_SCRIPT)
        subprocess.Popen([".\\update_poketerm.bat"], shell=True)
    else:
        # Write the Linux shell script
        with open('./update_poketerm.sh', 'w') as file:
            file.write(LINUX_SCRIPT)
            os.chmod('./update_poketerm.sh', 0o755)  # Make the shell script executable
        subprocess.Popen(['./update_poketerm.sh'])
    return True


WINDOWS_SCRIPT = """
@echo off
timeout /t 5 /nobreak >nul

set "OLD_APP_PATH=.\\PokeTerm.exe"
set "NEW_APP_PATH=.\\PokeTerm_Windows.exe"

:delete_old
if exist "%OLD_APP_PATH%" (
    del "%OLD_APP_PATH%"
    goto rename_new
) else (
    echo Old application not found.
    goto end
)

:rename_new
rename "%NEW_APP_PATH%" "PokeTerm.exe"
start "" ".\\PokeTerm.exe"
goto end

:end
"""

LINUX_SCRIPT = """
#!/bin/bash

sleep 5

OLD_APP_PATH="./PokeTerm"
NEW_APP_PATH="./PokeTerm_Linux"

if [ -f "$OLD_APP_PATH" ]; then
    rm "$OLD_APP_PATH"
fi

mv "$NEW_APP_PATH" "$OLD_APP_PATH"
chmod +x "$OLD_APP_PATH"
"$OLD_APP_PATH" &

exit 0
"""