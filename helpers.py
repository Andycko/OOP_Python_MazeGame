import os
import random
from sys import platform as _platform


def clear_console():
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        os.system("clear")
    elif _platform == "win32" or _platform == "win64":
        os.system("cls")
    else:
        print("Your platform is unfortunatelly not supported, see helpers.py")


def rock_paper_scissors():
    # TODO: Validate input
    print("You are playing a game of rock-paper-scissors!")
    bot = random.randint(1,3)
    player = input("Please input your choice in a form of number ranging from 1 to 3: ")

    if bot == player:
        print("Draw, play again please")
        rock_paper_scissors()
    elif bot == 1 and player == 2:
        return False
    elif bot == 2 and player == 3:
        return False
    elif bot == 3 and player == 1:
        return False
    else:
        return True


if __name__ == "__main__":
    clear_console()
