#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0

import random

from src.functions.getch1 import *
from src.characters.goblin import Goblin
from src.characters.monster import Monster


class Hero:
    """this is the hero class"""

    def __init__(self, name):
        """set the coordinate of the hero in the maze, name, coins, gems, src state"""
        self.name = name
        self._coordX = 2
        self._coordY = 2
        self._health = 100
        self._coins = 1000
        self._gems = 0
        self.aborted = False

    def __str__(self):
        """ Print Hero object overwriting """
        return "Your health is " + str(self._health) + "\nYou have " + str(self._coins) + " coins "\
                "and " + str(self._gems) + " gems"

    def get_gems(self):
        """ Gem getter function """
        return self._gems

    def get_coordinates(self):
        """ Coordinate getter function """
        return self._coordX, self._coordY

    def get_health(self):
        """ Health getter function """
        return self._health

    def get_coins(self):
        """ Coin getter function """
        return self._coins

    def set_coins(self, value):
        """ Coin setter function """
        self._coins = value

    def set_health(self, value):
        """ Health setter function """
        if 100 >= value > 0:
            self._health = value
        elif value <= 0:
            self._health = 0
        else:
            self._health = 100

    def give_gem(self):
        """ Gem increment function """
        self._gems += 1

    def take_health(self):
        """ Used to decrement 1 health / die"""
        if self._health > 1:
            self._health -= 1
            print(self)
            return True
        else:
            self._health = 0
            print(self)
            print("Your health has dropped to", self._health, ", you die now...")
            self.aborted = True
            return False

    def check_path(self, environment, direction):
        """ Checking if there is something in front of the hero before the character moves"""
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
        """ Identifying which creature is the monster/goblin in front of the hero"""
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
        if character == '\033':
            # I figured this is required on Unix because after the escape char there is also a "["
            getch()

        ch2 = getch()
        if ch2 == b'H' or ch2 == "A":
            # the up arrow key was pressed
            if self.check_path(environment, "top"):
                print("up key pressed")
                environment.set_coord(self._coordY, self._coordX, 0)
                self._coordY -= 1
                environment.set_coord(self._coordY, self._coordX, 2)
                return self.take_health()
            else:
                print("up key pressed - not a valid move")
                print(self)
                return False
        elif ch2 == b'P' or ch2 == "B":
            # the down arrow key was pressed
            if self.check_path(environment, "bottom"):
                print("down key pressed")
                environment.set_coord(self._coordY, self._coordX, 0)
                self._coordY += 1
                environment.set_coord(self._coordY, self._coordX, 2)
                return self.take_health()
            else:
                print("down key pressed - not a valid move")
                print(self)
                return False
        elif ch2 == b'K' or ch2 == "D":
            # the left arrow key was pressed
            if self.check_path(environment, "left"):
                print("left key pressed")
                environment.set_coord(self._coordY, self._coordX, 0)
                self._coordX -= 1
                environment.set_coord(self._coordY, self._coordX, 2)
                return self.take_health()
            else:
                print("left key pressed - not a valid move")
                print(self)
                return False
        elif ch2 == b'M' or ch2 == "C":
            # the right arrow key was pressed
            if self.check_path(environment, "right"):
                print("right key pressed")
                environment.set_coord(self._coordY, self._coordX, 0)
                self._coordX += 1
                environment.set_coord(self._coordY, self._coordX, 2)
                return self.take_health()
            else:
                print("right key pressed - Not a valid move")
                print(self)
                return False

        return False

    def spawn(self, maze):
        """ Spawn hero in the maze at random position"""
        self._coordY = random.randint(1, len(maze) - 2)
        self._coordX = random.randint(1, len(maze[self._coordY]) - 2)
        while maze[self._coordY][self._coordX] != 0:
            # I found this to be the most efficient way to ensure that there won't be an infinite loop
            list_row = random.sample(range(1, len(maze) - 1), len(maze) - 2)
            # Generate a list of unique random numbers for the row
            list_col = random.sample(range(1, len(maze[self._coordY]) - 1), len(maze[self._coordY]) - 2)
            # Generate a list of unique random numbers for the col
            for y in list_row:
                for x in list_col:
                    if maze[y][x] == 0:
                        self._coordX = x
                        self._coordY = y
                        maze[self._coordY][self._coordX] = 2
                        return maze

        maze[self._coordY][self._coordX] = 2
        return maze
