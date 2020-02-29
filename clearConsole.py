import os
from sys import platform as _platform


def clear_console():
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        os.system("clear")
    elif _platform == "win32" or _platform == "win64":
        os.system("cls")
    else:
        print("Your platform is unfortunatelly not supported, see clearConsole.py")


if __name__ == "__main__":
    clear_console()
