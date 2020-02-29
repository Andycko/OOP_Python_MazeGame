#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0

from getch1 import *
from clearConsole import clear_console
import sys, random


class Hero:
    """this is the hero class, further define it please"""
    def __init__(self):
        """set the coordinate of the hero in the maze"""

        self._coordX = 2
        self._coordY = 2
        self._health = 100
        self._coins = 1000  # gold coins the hero have.
        self._gem = 3
        self.aborted = False

    def health(self, show=False):
        if show:
            print("Your health is", self._health)
        elif self._health > 1:
            self._health -= 1
            print("Your health is", self._health)
            return True
        else:
            self._health -= 1
            print("Your health has dropped to 0, you die now...")
            self.aborted = True
            return False

    def move(self, environment):
        """move in the maze, it is noted this function may not work in the debug mode"""
        ch2 = getch()

        if ch2 == b'H' or ch2 == "A":
            # the up arrow key was pressed
            clear_console()
            print("up key pressed")
            return self.health()

        elif ch2 == b'P' or ch2 == "B":
            # the down arrow key was pressed
            clear_console()
            print("down key pressed")
            return self.health()

        elif ch2 == b'K' or ch2 == "D":
            # the left arrow key was pressed
            clear_console()
            print("left key pressed")
            return self.health()

        elif ch2 == b'M' or ch2 == "C":
            # the right arrow key was pressed
            clear_console()
            print("right key pressed")
            return self.health()

        elif ch2 == ':':    # Menu for user to use during the game
            command = input(":")
            if command == "exit":
                self.aborted = True
                clear_console()
                return False
            elif command == "help":
                print("Commands you can use:"
                      "\n\thelp\t- prints list of all commands"
                      "\n\tscore\t- prints your score"
                      "\n\texit\t- exits the game")
            elif command == "score":
                print("This is your score, whatever...")
            else:
                print("Sorry, not a valid command. Try inputing :help for list of commands")

        else:
            print("Sorry, not a valid input. Move with arrows and enter commands with \":\"")

        return False

    def move_debug(self, environment):

        """move in the maze, you need to press the enter key after keying in
        direction, and this works in the debug mode"""

        ch2 = sys.stdin.read(1)

        if ch2 == "w":
            # the up arrow key was pressed
            print("up key pressed")
            
            return True

        elif ch2 == "s":
            # the down arrow key was pressed
            print("down key pressed")
            return True

        elif ch2 == "a":
            # the left arrow key was pressed
            print("left key pressed")
            return True

        elif ch2 == "d":
            # the right arrow key was pressed
            print("right key pressed")
            return True

        return False

    def fight(self):
        """fight with monsters"""
        return

    def spawn(self, maze):
        self._coordY = random.randint(1, len(maze) - 2)
        self._coordX = random.randint(1, len(maze[self._coordY]) - 2)

        while maze[self._coordY][self._coordX] != 0:
            self._coordX = random.randint(1, len(maze[self._coordY]) - 2)

        maze[self._coordY][self._coordX] = 2
        return maze
