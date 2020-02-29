import os
from sys import platform as _platform


def clear_console():
    if _platform == "linux" or _platform == "darwin":
        os.system("clear")
    elif _platform == "win32" or _platform == "win64":
        os.system("cls")
    else:
        "Your platform is unfortunatelly not supported, see clearConsole.py"


clear_console()