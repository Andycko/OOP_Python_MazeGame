from copy import deepcopy
import pickle
import json
import textwrap

from src.functions.getch1 import *
from src.characters.goblin import Goblin
from src.functions.helpers import clear_console
from src.functions.helpers import get_terminal_size
from src.characters.hero import Hero
from src.functions.maze_gen_recursive import make_maze_recursion
from src.characters.monster import Monster

WALL_CHAR = "■"
SPACE_CHAR = " "
HERO_CHAR = "H"
GOBLIN_CHAR = "G"
MONSTER_CHAR = "M"


class _Environment:
    """Environment includes Maze with characters"""

    def __init__(self, maze):
        self._environment = deepcopy(maze)

    def set_coord(self, x, y, val):
        """ Value setter method at certain coordinates """
        self._environment[x][y] = val

    def get_coord(self, x, y):
        """ Value getter method at certain coordinates """
        return self._environment[x][y]

    def update_environment(self, hero):
        """ Updates monsters and goblins in the maze """
        for monster in Monster.all_monsters:
            coordx, coordy = monster.get_coordinates()
            h_coordx, h_coordy = hero.get_coordinates()
            if coordx == h_coordx and coordy == h_coordy:
                # if hero and moster colide, let hero be on that place, but monster will retain its coordinates
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
        if difficulty == "load":  # If the player decides to load instead of a new src, call load_game() method
            if not self.load_game():
                exit()
        else:
            self.difficulty = difficulty
            self.myHero = Hero(name)
            self.maze = make_maze_recursion(17, 17, difficulty)  # returning maze with monsters and goblins
            self.maze = self.myHero.spawn(self.maze)  # Spawning hero, returning maze with the hero in it
            self.MyEnvironment = _Environment(self.maze)  # Environment is the maze with all characters
            self._count = 0

    def menu(self):
        """ Opens a command prompt waiting for input, the src can be controlled from here by the user """
        command = input(":")
        command = command.lower()
        if command == "help":
            print("Commands you can use:"
                  "\n\thelp\t- prints list of all commands"
                  "\n\tscoreboard\t- prints your score"
                  "\n\tmap\t- prints out the map of the current maze"
                  "\n\tsave\t- save the current state of the src"
                  "\n\texit\t- exits the src")
        elif command == "scoreboard":
            print("This is the current scoreboard, to be in it, finish your src first.")
            self.print_scoreboard()
        elif command == "map":
            self.MyEnvironment.print_environment(self.myHero)
        elif command == "save":
            self.save_game()
        elif command == "exit":
            self.myHero.aborted = True
            clear_console()
        else:
            print("Sorry, not a valid command. Try inputting :help for list of commands")

    def save_game(self):
        """ Saving data from the src to a pickle file """
        print("...saving the src")
        save = {
            "hero": self.myHero,
            "all_monsters": Monster.all_monsters,
            "visited_monsters": Monster.visited_monsters,
            "all_goblins": Goblin.all_goblins,
            "environment": self.MyEnvironment,
            "difficulty": self.difficulty,
            "move_count": self._count
        }
        pickle.dump(save, open("files/save_file.dat", "wb"))
        clear_console()
        print("...your src has been successfully saved")
        print(self.myHero)
        self.MyEnvironment.print_environment(self.myHero)

    def load_game(self):
        """ Loading data from a pickle file """
        print("...loading src from the last save")
        try:
            load = pickle.load(open("files/save_file.dat", "rb"))
            self.myHero = load.get("hero")
            Monster.all_monsters = load.get("all_monsters")
            Monster.visited_monsters = load.get("visited_monsters")
            Goblin.all_goblins = load.get("all_goblins")
            self.MyEnvironment = load.get("environment")
            self.difficulty = load.get("difficulty")
            self._count = load.get("move_count")
        except FileNotFoundError:
            print("There is no valid last save of the src. Please start a new one.")
            return False
        except ModuleNotFoundError:
            return False

        clear_console()
        print("...your src has been successfully loaded")
        print(self.myHero)
        self.MyEnvironment.print_environment(self.myHero)
        return True

    def save_score(self):
        """ Save score of the current src to the scoreboard """
        with open("files/scoreboard.json") as scoreboard:
            data = json.load(scoreboard)
            data[self.difficulty].append({"player": {"name": self.myHero.name, "score": self.myHero.get_coins()}})

        with open("files/scoreboard.json", 'w') as f:
            json.dump(data, f, indent=4)

    def print_scoreboard(self):
        """ Load the scoreboard and print it"""
        with open("files/banner.txt", "r") as f:
            for x in f:
                print(x, end="")

        with open("files/scoreboard.json") as scoreboard:
            data = json.load(scoreboard)
            count = 1
            players = {}
            print("+++++++++++++++++++++++++++++")
            for diff in data:
                # Going through all the players in json data, checking for duplicate names while copying to a dictionary
                print("\n  " + str(diff.upper()) + ":")
                rep = 1
                for player in data[diff]:
                    name = player["player"]["name"]
                    while name in players:
                        rep += 1
                        name = player["player"]["name"] + str(rep)

                    rep = 1
                    players[name] = player["player"]["score"]

                # part of next line copied from https://ide.geeksforgeeks.org/5Ttw73QBJ0 and modified
                for player in sorted(players.items(), key=lambda kv: (kv[1], kv[0]))[::-1]:
                    # sorting the players based on the highest score
                    if len(player[0]) <= 1:
                        tab = "\t\t"
                    else:
                        tab = "\t"
                    print("  " + str(count) + ".", player[0], tab, player[1])
                    count += 1

                count = 0
                players = {}
                print("\n+++++++++++++++++++++++++++++")

    def play(self, loaded=False):
        """ Main method of the Game class, starts the src and controls the src when it runs """
        if loaded:  # loaded is true when the player chooses to load an existing src at the start
            clear_console()
            print(self.myHero)  # Just showing the health and the coins of hero at the start of the src
            self.MyEnvironment.print_environment(self.myHero)
            print("\nMoves made:", self._count)

        while (not self.myHero.aborted) and (self.myHero.get_gems() < 5):
            # Checking if player has not aborted the src with :exit command or died
            ch = getch()
            if ch == '\033' or ch == b'\xe0':  # Checking if player is pressing arrow keys
                clear_console()
                if self.myHero.move(self.MyEnvironment, ch):
                    self._count += 1
                self.MyEnvironment.print_environment(self.myHero)
                print("\nMoves made:", self._count)
            else:
                if ch == b':' or ch == ":":  # Checking if player inputs : for command input
                    self.menu()
                else:  # If not : then it is not a valid input
                    print("Sorry, not a valid input. Move with arrows and enter commands with \":\"")

        if not self.myHero.aborted:
            print("Congratulations mighty warrior, you defeated all the monsters and collected all your missing gems!",
                  "\nFeel free to find your name on the scoreboard.")
            self.save_score()
            self.print_scoreboard()
            print("Thank you for playing the Maze Game made by Andrej Szalma! Feel free to check out the code on my"
                  "github -> https://github.com/Andycko/OOP_Python_MazeGame")
        else:
            self.print_scoreboard()
            print("Thank you for playing the Maze Game made by Andrej Szalma! Feel free to check out the code on my"
                  "github -> https://github.com/Andycko/OOP_Python_MazeGame")


def welcome_screen():
    """ Function to show the welcome screen with all the prompts before the src starts.
        Not in the Game class as input from this function is needed for the Game __init__ """
    clear_console()
    with open("files/banner.txt", "r") as f:
        for x in f:
            print(x, end="")

    state = input("Welcome, would you like to start a new src or load an existing one? [new, load]: ")
    while state not in ["new", "load"]:
        state = input("Welcome, would you like to start a new src or load an existing one? [new, load]: ")
    if state == "load":
        return "load"

    name = input("Please tell me your name brave warrior: ")

    message = "\nWelcome in the Maze Game " + str(name) + "," \
        "\nYou have been researching the ruins of the haunted castle Barrowhaven on your " \
        "quest to find the lost treasures of the Kingdom Of Glauvia. So far you have defeated orcs, strigas, vampires" \
        ", vukolaks and many other malicious creatures. But you never fought more than one at a time. However, this " \
        "time, there were many of them. Monsters they were.\n\nThe last thing you remember is getting punched in the " \
        "head and you have now woken up in this maze. A maze without an exit. You soon realize that you are hurt and " \
        "that your gems have been stolen. There is no way you could continue your journey without them, therefore you" \
        " need to find all the monsters and get your gems. There are 5 gems in total and you can get them by" \
        " interacting with a monster. But think twice before you start your quest, because every" \
        " step will cost you 1 health. You might also stumble across different types of creatures, be careful! " \
        "Get back all your gems and you can leave the maze.\n\nDon't forget the hero with the most coins at the end " \
        "gets the highest score. You can move through the maze with your arrows and use \":\" to enter commands.\n\n" \
        "Enough talking now, you should get going. May good luck be on your side!\n"

    term_width, term_height = get_terminal_size()
    wrapped_message = textwrap.fill(message, width=term_width * 0.9, replace_whitespace=False)
    print(wrapped_message)

    difficulty = input("\nPlease pick a level of difficulty [easy, medium, hard]: ")
    while difficulty not in ["easy", "medium", "hard"]:
        print("Please input a valid level of difficulty")
        difficulty = input("Please pick a level of difficulty [easy, medium, hard]: ")

    return difficulty, name


def launch_game():
    """ use this function to launch the src"""
    out = welcome_screen()
    if len(out) == 2:
        my_game = Game(out[0], out[1])
        my_game.play(True)
    else:
        my_game = Game(out)
        my_game.play()
