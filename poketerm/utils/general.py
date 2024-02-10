import platform


# region Version Checks
def is_windows():
    return platform.system() == "Windows"


def IsLinuxOS():
    return platform.system() == "Linux"


def IsMacOS():
    return platform.system() == "Darwin"


# endregion
