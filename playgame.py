from copy import deepcopy

from getch1 import *
from goblin import Goblin
from helpers import clear_console
from hero import Hero
from maze_gen_recursive import make_maze_recursion
from monster import Monster

WALL_CHAR = "■"
SPACE_CHAR = " "
HERO_CHAR = "H"
GOBLIN_CHAR = "G"
MONSTER_CHAR = "M"


class _Environment:
    """Environment includes Maze"""

    def __init__(self, maze):
        self._environment = deepcopy(maze)

    def set_coord(self, x, y, val):
        self._environment[x][y] = val

    def get_coord(self, x, y):
        return self._environment[x][y]

    def update_environment(self, hero):
        """ Updates monsters and goblins in the maze """
        for monster in Monster.all_monsters:
            coordx, coordy = monster.get_coordinates()
            h_coordx, h_coordy = hero.get_coordinates()
            if coordx == h_coordx and coordy == h_coordy:
                continue
            self._environment[coordy][coordx] = 4

        for goblin in Goblin.all_goblins:
            coordx, coordy = goblin.get_coordinates()
            self._environment[coordy][coordx] = 3

    def print_environment(self, hero):
        """ Print out the environment in the terminal """

        self.update_environment(hero)
        for row in self._environment:
            row_str = str(row)
            row_str = row_str.replace("1", WALL_CHAR)  # replace the wall character
            row_str = row_str.replace("0", SPACE_CHAR)  # replace the space character
            row_str = row_str.replace("2", HERO_CHAR)  # replace the hero character
            row_str = row_str.replace("3", GOBLIN_CHAR)  # replace the hero character
            row_str = row_str.replace("4", MONSTER_CHAR)  # replace the hero character

            print("".join(row_str)[1:-1].replace(",", ""))


class Game:
    _count = 0

    def __init__(self, difficulty):
        self.myHero = Hero()
        # self.monsters, self.goblins, self.maze = make_maze_recursion(20, 20)
        self.maze = make_maze_recursion(20, 20, difficulty)
        self.maze = self.myHero.spawn(self.maze)  # Spawning hero, returning maze with the hero in it
        self.MyEnvironment = _Environment(self.maze)  # initial environment is the maze itself
        self._count = 0

    def menu(self):
        """ Opens a command prompt waiting for input, the game can be controlled from here by the user """
        command = input(":")
        if command == "exit":
            self.myHero.aborted = True
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
            print("Sorry, not a valid command. Try inputting :help for list of commands")

    def play(self):
        self.myHero.health(show=True)  # Just showing the health at the start of game
        self.MyEnvironment.print_environment(self.myHero)
        print("============================", self._count)  # Leaving this here just for debugging purposes

        while not self.myHero.aborted:  # Checking if player has not aborted the game with :exit command or died
            # if self.myHero.move_debug(self.MyEnvironment):  #this works in debug mode
            ch = getch()
            if ch == '\033' or ch == b'\xe0':  # Checking if player is pressing arrow keys
                clear_console()
                self.myHero.move(self.MyEnvironment, ch)
                self.MyEnvironment.print_environment(self.myHero)
                self._count += 1
                print("============================", self._count)
            else:
                if ch == b':' or ch == ":":  # Checking if player inputs : for command input
                    self.menu()
                else:  # If not : then it is not a valid input
                    print("Sorry, not a valid input. Move with arrows and enter commands with \":\"")


if __name__ == "__main__":
    myGame = Game(input("Please pick a level of difficulty [easy, medium, hard]: "))
    myGame.play()
