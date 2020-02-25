#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0

from getch1 import *
import os
import sys


class Hero:
    """this is the hero class, further define it please"""
    def __init__(self):
        """set the coordinate of the hero in the maze"""
        self._coordX = 2
        self._coordY = 2
        self._health = 100
        self._coins = 1000  # gold coins the hero have.
        self._gem=3
        self._aborted = False


    def health(self):
        if self._health > 1:
            self._health -= 1
            print("Your health is", self._health)
            return True
        else:
            self._health -= 1
            print("Your health has dropped to 0, you die now...")
            self._aborted = True
            return False

    def move(self, environment):
        """move in the maze, it is noted this function may not work in the debug mode"""
        ch2 = getch()

        if ch2 == b'H' or ch2 == "A":
            # the up arrow key was pressed
            os.system("cls")
            print ("up key pressed")
            return self.health()



        elif ch2 == b'P' or ch2 == "B":
            # the down arrow key was pressed
            os.system("cls")
            print("down key pressed")
            return self.health()


        elif ch2 == b'K' or ch2 == "D":
            # the left arrow key was pressed
            os.system("cls")
            print("left key pressed")
            return self.health()

        elif ch2 == b'M' or ch2 == "C":
            # the right arrow key was pressed
            os.system("cls")
            print("right key pressed")
            return self.health()
        
        elif ch2 == b'\x1b':
            self._aborted = True
            os.system("cls")
            return False

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


