from copy import deepcopy
import pickle
import textwrap

from getch1 import *
from goblin import Goblin
from helpers import clear_console
from helpers import get_terminal_size
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

    def __init__(self, difficulty, name=""):
        if difficulty == "load":
            if not self.load_game():
                exit()
        else:
            self.difficulty = difficulty
            self.myHero = Hero(name)
            self.maze = make_maze_recursion(17, 17, difficulty)
            self.maze = self.myHero.spawn(self.maze)  # Spawning hero, returning maze with the hero in it
            self.MyEnvironment = _Environment(self.maze)  # initial environment is the maze itself
            self._count = 0

    def menu(self):
        """ Opens a command prompt waiting for input, the game can be controlled from here by the user """
        command = input(":")
        command = command.lower()
        if command == "help":
            print("Commands you can use:"
                  "\n\thelp\t- prints list of all commands"
                  "\n\tscore\t- prints your score"
                  "\n\tsave\t- save the current state of the game"
                  "\n\tload\t- load previously saved game"
                  "\n\texit\t- exits the game")
        elif command == "score":
            print("This is your score, whatever...")
        elif command == "load":
            self.load_game()
        elif command == "save":
            self.save_game()
        elif command == "exit":
            self.myHero.aborted = True
            clear_console()
            return False
        else:
            print("Sorry, not a valid command. Try inputting :help for list of commands")

    def save_game(self):
        print("...saving the game")
        save = {"hero": self.myHero,
                "all_monsters": Monster.all_monsters,
                "visited_monsters": Monster.visited_monsters,
                "all_goblins": Goblin.all_goblins,
                "environment": self.MyEnvironment,
                "difficulty": self.difficulty}
        pickle.dump(save, open("save_file.dat", "wb"))
        clear_console()
        print("...your game has been successfully saved")
        print(self.myHero)
        self.MyEnvironment.print_environment(self.myHero)

    def load_game(self):
        print("...loading game from the last save")
        try:
            load = pickle.load(open("save_file.dat", "rb"))
            self.myHero = load.get("hero")
            Monster.all_monsters = load.get("all_monsters")
            Monster.visited_monsters = load.get("visited_monster")
            Goblin.all_goblins = load.get("all_goblins")
            self.MyEnvironment = load.get("environment")
            self.difficulty = load.get("difficulty")
        except FileNotFoundError:
            print("There is no valid last save of the game. Please start a new one or save your current game.")
            return False

        clear_console()
        print("...your game has been successfully loaded")
        print(self.myHero)
        self.MyEnvironment.print_environment(self.myHero)
        return True

    def play(self, loaded=False):
        if loaded:
            clear_console()
            print(self.myHero)  # Just showing the health and the coins of hero at the start of the game
            self.MyEnvironment.print_environment(self.myHero)
            print("============================", self._count)  # Leaving this here just for debugging purposes

        while (not self.myHero.aborted) and (self.myHero.get_gems() < 5):
            # Checking if player has not aborted the game with :exit command or died
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

        if not self.myHero.aborted:
            print("Congratulations mighty warrior, you defeated all the monsters and collected all your missing gems!",
                  "\nFeel free to find your name on the scoreboard.")


def welcome_screen():
    clear_console()
    with open("banner.txt", "r") as f:
        for x in f:
            print(x, end="")

    state = input("Welcome, would you like to start a new game or load an existing one? [new, load]: ")
    while state not in ["new", "load"]:
        state = input("Welcome, would you like to start a new game or load an existing one? [new, load]: ")
    if state == "load":
        return "load"

    name = input("Please tell me your name brave warrior: ")

    message = "\nWelcome in the Maze Game " + str(name) + ","\
        "\nYou have been researching the ruins of the haunted castle Barrowhaven on your"\
        "quest to find the lost treasures of the Kingdom Of Glauvia. So far you have defeated orcs, strigas, vampires"\
        ", vukolaks and many other malicious creatures. But you never fought more than one at a time. However, this "\
        "time, there were many of them. Monsters they were.\n\nThe last thing you remember is getting punched in the "\
        "head and you have now woken up in this maze. A maze without an exit. You soon realise that you are hurt and "\
        "that your gems have been stolen. There is no way you could continue your journey without them, therefore you"\
        " need to find all the monsters and get your gems. But think twice before you start your quest, because every"\
        " step will cost you 1 health. You might also stumble across different types of creatures, be careful!"\
        "Get back all your gems and you can leave the maze.\n\nDon't forget the hero with the most coins at the end "\
        "gets the highest score. You can move through the maze with your arrows and use \":\" to enter commands. "\
        "\n\nEnough talking now, you should get going. May good luck be on your side!\n"

    term_width, term_height = get_terminal_size()
    wrapped_message = textwrap.fill(message, width=term_width * 0.9, replace_whitespace=False)
    print(wrapped_message)

    difficulty = input("\nPlease pick a level of difficulty [easy, medium, hard]: ")
    while difficulty not in ["easy", "medium", "hard"]:
        print("Please input a valid level of difficulty")
        difficulty = input("Please pick a level of difficulty [easy, medium, hard]: ")

    return difficulty, name


if __name__ == "__main__":
    out = welcome_screen()
    if len(out) == 2:
        myGame = Game(out[0], out[1])
        myGame.play(True)
    else:
        myGame = Game(out)
        myGame.play()
