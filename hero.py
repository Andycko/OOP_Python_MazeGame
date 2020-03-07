#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0

import random
import sys

from getch1 import *
from goblin import Goblin
from helpers import clear_console
from monster import Monster


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

    def get_coordinates(self):
        return self._coordX, self._coordY

    def get_health(self):
        return self._health

    def get_coins(self):
        return self._coins

    def set_coins(self, value):
        self._coins = value

    def set_health(self, value):
        if 100 >= value > 0:
            self._health = value
        elif value <= 0:
            self._health = 0
        else:
            self._health = 100

    def health(self, show=False):
        if show:
            print("Your health is", self._health)
        elif self._health > 1:
            self._health -= 1
            print("Your health is", self._health)
            return True
        else:
            self._health = 0
            print("Your health has dropped to", self._health, ", you die now...")
            self.aborted = True
            return False

    def check_path(self, environment, direction):
        if direction == "top":
            x = 0
            y = -1
        elif direction == "bottom":
            x = 0
            y = 1
        elif direction == "right":
            x = 1
            y = 0
        elif direction == "left":
            x = -1
            y = 0
        else:
            print("Wrong direction passed to the check_path function")
            return False

        if environment.get_coord(self._coordY + y, self._coordX + x) == 0:
            return True
        elif environment.get_coord(self._coordY + y, self._coordX + x) == 4:
            monster = self.identify_creature(self._coordX + x, self._coordY + y, monster=True)
            if type(monster).__name__ == "FighterMonster":
                monster.fight(self)
                return True
            elif type(monster).__name__ == "ThiefMonster":
                monster.steal(self)
                return True
            else:
                monster.play(self)
                return True

        elif environment.get_coord(self._coordY + y, self._coordX + x) == 3:
            goblin = self.identify_creature(self._coordX + x, self._coordY + y, goblin=True)
            if type(goblin).__name__ == "WealthGoblin":
                goblin.give_coin(self)
                goblin.destroy()
                return True
            elif type(goblin).__name__ == "HealthGoblin":
                goblin.give_health(self)
                goblin.destroy()
                return True
            else:
                goblin.play(self)
                goblin.destroy()
                return True

        else:
            return False

    def identify_creature(self, coord_x, coord_y, monster=False, goblin=False):
        if monster:
            for monster in Monster.all_monsters:
                x, y = monster.get_coordinates()
                if (coord_x == x) and (coord_y == y):
                    return monster
        elif goblin:
            for goblin in Goblin.all_goblins:
                x, y = goblin.get_coordinates()
                if (coord_x == x) and (coord_y == y):
                    return goblin
        else:
            print("Need to be a monster or a goblin")

    def move(self, environment, character):
        """move in the maze, it is noted this function may not work in the debug mode"""
        if character == '\033':  # I figured this is required on Unix because after the escape char there is also a "["
            getch()

        ch2 = getch()
        if ch2 == b'H' or ch2 == "A":
            # the up arrow key was pressed
            # clear_console()
            print("up key pressed - ", end="")
            if self.check_path(environment, "top"):
                environment.set_coord(self._coordY, self._coordX, 0)
                self._coordY -= 1
                environment.set_coord(self._coordY, self._coordX, 2)
                return self.health()
            else:
                print("Not a valid move")
                self.health(show=True)
                return True
        elif ch2 == b'P' or ch2 == "B":
            # the down arrow key was pressed
            # clear_console()
            print("down key pressed - ", end="")
            if self.check_path(environment, "bottom"):
                environment.set_coord(self._coordY, self._coordX, 0)
                self._coordY += 1
                environment.set_coord(self._coordY, self._coordX, 2)
                return self.health()
            else:
                print("Not a valid move")
                self.health(show=True)
                return True
        elif ch2 == b'K' or ch2 == "D":
            # the left arrow key was pressed
            # clear_console()
            print("left key pressed - ", end="")
            if self.check_path(environment, "left"):
                environment.set_coord(self._coordY, self._coordX, 0)
                self._coordX -= 1
                environment.set_coord(self._coordY, self._coordX, 2)
                return self.health()
            else:
                print("Not a valid move")
                self.health(show=True)
                return True
        elif ch2 == b'M' or ch2 == "C":
            # the right arrow key was pressed
            # clear_console()
            print("right key pressed - ", end="")
            if self.check_path(environment, "right"):
                environment.set_coord(self._coordY, self._coordX, 0)
                self._coordX += 1
                environment.set_coord(self._coordY, self._coordX, 2)
                return self.health()
            else:
                print("Not a valid move")
                self.health(show=True)
                return True

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

    def spawn(self, maze):  # Adding Goblins and Monsters to the maze recursively
        self._coordY = random.randint(1, len(maze) - 2)
        self._coordX = random.randint(1, len(maze[self._coordY]) - 2)
        while maze[self._coordY][self._coordX] != 0:
            # Continue as long as don't find a 0 in the maze
            # I found this to be the most efficient way to ensure that there won't be an infinite loop
            list_row = random.sample(range(1, len(maze) - 1),
                                     len(maze) - 2)  # Generate a list of unique random numbers for the row
            list_col = random.sample(range(1, len(maze[self._coordY]) - 1), len(
                maze[self._coordY]) - 2)  # Generate a list of unique random numbers for the col
            for y in list_row:
                for x in list_col:
                    if maze[y][x] == 0:
                        self._coordX = x
                        self._coordY = y
                        maze[self._coordY][self._coordX] = 2
                        return maze

        maze[self._coordY][self._coordX] = 2
        return maze
