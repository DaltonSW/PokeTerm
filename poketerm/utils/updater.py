import subprocess
import os

from poketerm.utils.general import is_windows
from poketerm.utils.visual import clear_screen
import poketerm.config
import requests

from readchar import readkey, key as keys

from poketerm.console import console
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


def delete_existing_updaters() -> None:
    if os.path.exists("update_poketerm.bat"):
        os.remove("update_poketerm.bat")

    if os.path.exists("update_poketerm.sh"):
        os.remove("update_poketerm.sh")


def get_latest_version_from_github():
    req = requests.get("https://github.com/DaltonSW/PokeTerm/releases/latest")
    if req.status_code != 200:
        console.print("Couldn't connect to repository. Returning.")
        return None

    try:
        return req.url.split("/")[-1]
    except IndexError:
        console.print("Invalid URL loaded. Returning.")
        return None


def is_newer_version(version: str) -> bool:
    appMajor, appMinor, appPatch = poketerm.config.APP_VERSION.split(".")
    latestMajor, latestMinor, latestPatch = version.split(".")

    if latestMajor > appMajor:
        return True

    if latestMajor == appMajor and latestMinor > appMinor:
        return True

    if latestMajor == appMajor and latestMinor == appMinor and latestPatch > appPatch:
        return True

    return False


def check_for_update() -> bool:
    delete_existing_updaters()

    clear_screen()

    latestVersion = get_latest_version_from_github()

    if latestVersion is None or not is_newer_version(latestVersion):
        return False

    return prompt_for_update(latestVersion)


def prompt_for_update(newVersion) -> bool:
    console.print("New version found! Press \[Enter] to download.")
    key = readkey()
    if key == keys.ENTER:
        return download_update(newVersion)
    return False


def get_update_URL(version: str) -> (str, str):
    fileName = "PokeTerm_" + "Windows.exe" if is_windows() else "PokeTerm_" + "Linux"
    return (
        f"https://github.com/DaltonSW/PokeTerm/releases/download/{version}/{fileName}",
        fileName,
    )


# Rich Progress bar implementation derived from Will McGugan's example
# https://github.com/Textualize/rich/blob/master/examples/downloader.py#L47
def download_update(version: str) -> bool:
    downloadURL, fileName = get_update_URL(version)
    chunkSize = 32768

    try:
        with requests.get(downloadURL, stream=True) as downloadRequest:
            if downloadRequest.status_code != 200:
                console.print("Couldn't download PokeTerm. Returning")
                return False

            with progress:
                downloadTaskID = progress.add_task(
                    f"Downloading PokeTerm v{version}",
                    total=int(downloadRequest.headers.get("Content-Length", 0)),
                    filename=fileName,
                )
                with open(f".{os.sep}'new'{fileName}", "wb") as newFile:
                    for data in downloadRequest.iter_content(chunk_size=chunkSize):
                        newFile.write(data)
                        progress.update(downloadTaskID, advance=chunkSize)

        console.print("New version downloaded! Press \[Enter] to restart the program.")
        key = readkey()
        if key == keys.ENTER:
            return create_update_script_and_update()
        return False

    except PermissionError:
        console.clear()
        console.print(
            "Insufficient permissions. Run the application as administrator and try again."
        )
        _ = readkey()


def create_update_script_and_update():
    if is_windows():
        with open(".\\update_poketerm.bat", "w") as file:
            file.write(WINDOWS_SCRIPT)
        subprocess.Popen([".\\update_poketerm.bat"], shell=True)
    else:
        # Write the Linux shell script
        with open("./update_poketerm.sh", "w") as file:
            file.write(LINUX_SCRIPT)
            os.chmod("./update_poketerm.sh", 0o755)  # Make the shell script executable
        subprocess.Popen(["./update_poketerm.sh"])
    return True


# Both of these scripts were obtained from ChatGPT
WINDOWS_SCRIPT = """
@echo off
timeout /t 5 /nobreak >nul

set "OLD_APP_PATH1=.\\PokeTerm.exe"
set "OLD_APP_PATH2=.\\PokeTerm_Windows.exe"
set "NEW_APP_PATH=.\\newPokeTerm_Windows.exe"

if exist "%OLD_APP_PATH1%" (
    del "%OLD_APP_PATH1%"
)
if exist "%OLD_APP_PATH2%" (
    del "%OLD_APP_PATH2%"
)

if exist "%NEW_APP_PATH%" (
    rename "%NEW_APP_PATH%" "PokeTerm.exe"
    start "" ".\\PokeTerm.exe"
) else (
    echo New application not found.
)
"""

LINUX_SCRIPT = """
#!/bin/bash

sleep 5

OLD_APP_PATH="./PokeTerm"
NEW_APP_PATH="./newPokeTerm_Linux"

# Check if either PokeTerm or PokeTerm_Linux exists and remove it
if [ -f "$OLD_APP_PATH" ] || [ -f "${OLD_APP_PATH}_Linux" ]; then
    rm -f "$OLD_APP_PATH" "${OLD_APP_PATH}_Linux"
fi

mv "$NEW_APP_PATH" "$OLD_APP_PATH"
chmod +x "$OLD_APP_PATH"
"$OLD_APP_PATH" &

exit 0
"""
