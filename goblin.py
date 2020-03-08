#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0
import random

from helpers import rock_paper_scissors


class Goblin:
    all_goblins = []  # All goblin objects are stored here

    def __init__(self, coord_x, coord_y, difficulty):
        self._coordX = coord_x
        self._coordY = coord_y
        if difficulty == "hard":
            self._difficulty = 0.5
        elif difficulty == "medium":
            self._difficulty = 0.75
        else:
            self._difficulty = 1
        Goblin.all_goblins.append(self)

    def get_coordinates(self):
        """ Coordinates getter method """
        return self._coordX, self._coordY

    def destroy(self):
        """ Method called after goblin meets the hero """
        Goblin.all_goblins.remove(self)


class WealthGoblin(Goblin):

    def __init__(self, coord_x, coord_y, difficulty):
        super(WealthGoblin, self).__init__(coord_x, coord_y, difficulty)
        self._coins = random.randint(10, 300)
        self._probability = round(((400 - self._coins) * self._difficulty) / 4)

    def give_coin(self, hero):
        """ Main interaction method of this Goblin """
        print("You have met a Wealth goblin with", self._coins, "coins to give and", str(self._probability) +
              "% probability to give them to you")
        probability_list = range(1, self._probability + 1)  # list of numbers stating the probability
        if random.randint(1, 100) in probability_list:  # random number N = <1;100> check if is in probability_list
            hero.set_coins(hero.get_coins() + self._coins)
            print("You have received", self._coins, "coins, your have now", hero.get_coins(), "coins\n")
        else:
            print("You are unlucky, the goblin did not give you any coin.\n")


class HealthGoblin(Goblin):
    def __init__(self, coord_x, coord_y, difficulty):
        super(HealthGoblin, self).__init__(coord_x, coord_y, difficulty)
        self._health = random.randint(1, 50)
        self._probability = round((100 - self._health) * self._difficulty)

    def give_health(self, hero):
        """ Main interaction method of this Goblin """
        print("You have met a Healer goblin with", self._health, "heal and", str(self._probability) +
              "% probability to heal you")
        probability_list = range(1, self._probability + 1)  # list of numbers stating the probability
        if random.randint(1, 100) in probability_list:  # random number N = <1;100> check if is in probability_list
            hero.set_health(hero.get_health() + self._health)
            print("The goblin has healed by", self._health, "health, your have now", hero.get_health(), "health\n")
        else:
            print("You are unlucky, the goblin did not heal you.\n")


class GamerGoblin(Goblin):
    def __init__(self, coord_x, coord_y, difficulty):
        super(GamerGoblin, self).__init__(coord_x, coord_y, difficulty)
        self._health = random.randint(1, 50)
        self._coins = random.randint(10, 300)

    def play(self, hero):
        """ Main interaction method of this Goblin """
        print("You have met a Gamer goblin with", self._health, "heal and", self._coins, "coins to give")
        if rock_paper_scissors():  # using my RPS function from helpers.py
            print("You lost, you don't get anything from this goblin.\n")
        else:
            hero.set_coins(hero.get_coins() + self._coins)
            hero.set_health(hero.get_health() + self._health)
            print("You received", self._coins, "coins and", self._health, "health, you have", hero.get_coins(),
                  "coins and", hero.get_health(), "health\n")
