from hero import Hero
from maze_gen_recursive import make_maze_recursion
from copy import deepcopy

WALL_CHAR = "#"
SPACE_CHAR = "-"
HERO_CHAR = "H"


class _Environment:
    """Environment includes Maze+Monster+Goblin"""
    def __init__(self, maze):
        self._environment = deepcopy(maze)

    def set_coord(self, x, y, val):
        self._environment[x][y] = val

    def get_coord(self, x, y):
        return self._environment[x][y]

    def print_environment(self):
        """print out the environment in the terminal"""
        for row in self._environment:
            row_str = str(row)
            row_str = row_str.replace("1", WALL_CHAR)  # replace the wall character
            row_str = row_str.replace("0", SPACE_CHAR)  # replace the space character
            row_str = row_str.replace("2", HERO_CHAR)  # replace the hero character

            print("".join(row_str))


class Game:

    _count = 0

    def __init__(self):
        self.myHero = Hero()
        self.maze = make_maze_recursion(7, 7)
        self.MyEnvironment = _Environment(self.maze)  # initial environment is the maze itself
        self._count = 0

    def play(self):
        while self.myHero._aborted == False:

            if self.myHero.move(self.MyEnvironment):
            #if self.myHero.move_debug(self.MyEnvironment):  #this works in debug mode
                self.MyEnvironment.print_environment()
                self._count += 1
                print("============================", self._count)


if __name__ == "__main__":

    myGame = Game()
    myGame.play()
    