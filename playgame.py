from hero import Hero
from monster import Monster
from goblin import Goblin
from maze_gen_recursive import make_maze_recursion
from copy import deepcopy

WALL_CHAR = "■"
SPACE_CHAR = " "
HERO_CHAR = "H"
GOBLIN_CHAR = "G"
MONSTER_CHAR = "M"


class _Environment:
    """Environment includes Maze+Monster+Goblin"""
    def __init__(self, maze):
        self._environment = deepcopy(maze)

    def set_coord(self, x, y, val):
        self._environment[x][y] = val

    def get_coord(self, x, y):
        return self._environment[x][y]

    def print_environment(self, hero):
        """print out the environment in the terminal"""
        for monster in Monster.all_monsters:
            coordx, coordy = monster.get_coordinates()
            h_coordx, h_coordy = hero.get_coordinates()
            if coordx == h_coordx and coordy == h_coordy:
                continue
            self._environment[coordy][coordx] = 4

        for goblin in Goblin.all_goblins:
            coordx, coordy = goblin.get_coordinates()
            self._environment[coordy][coordx] = 3

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

    def __init__(self):
        self.myHero = Hero()
        # self.monsters, self.goblins, self.maze = make_maze_recursion(20, 20)
        self.maze = make_maze_recursion(20, 20)
        self.maze = self.myHero.spawn(self.maze)    # Spawning hero, returning maze with the hero in it
        self.MyEnvironment = _Environment(self.maze)  # initial environment is the maze itself
        self._count = 0

    def play(self):
        self.myHero.health(show=True)   # Just showing the health at the start of game
        self.MyEnvironment.print_environment(self.myHero)
        print("============================", self._count)  # Leaving this here just for debugging purposes

        while not self.myHero.aborted:  # Checking if player has not aborted the game with :exit command or died
            # if self.myHero.move_debug(self.MyEnvironment):  #this works in debug mode
            if self.myHero.move(self.MyEnvironment):
                self.MyEnvironment.print_environment(self.myHero)
                self._count += 1
                print("============================", self._count)


if __name__ == "__main__":

    myGame = Game()
    myGame.play()
