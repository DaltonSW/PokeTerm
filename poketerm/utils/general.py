import platform


# region Version Checks
def IsWindowsOS():
    return platform.system() == "Windows"


def IsLinuxOS():
    return platform.system() == "Linux"


def IsMacOS():
    return platform.system() == "Darwin"


# endregion
