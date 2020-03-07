#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0
import random

from helpers import rock_paper_scissors


class Goblin:
    all_goblins = []

    def __init__(self, coord_x, coord_y, difficulty):
        self._coordX = coord_x
        self._coordY = coord_y
        if difficulty == "hard":
            self._difficulty = 0.6
        elif difficulty == "medium":
            self._difficulty = 0.9
        else:
            self._difficulty = 1.2
        Goblin.all_goblins.append(self)

    def get_coordinates(self):
        return self._coordX, self._coordY

    # def __del__(self):
    # this does not work for some reason
    #     Goblin.all_goblins.remove(self)

    def destroy(self):
        Goblin.all_goblins.remove(self)


class WealthGoblin(Goblin):
    def __init__(self, coord_x, coord_y, difficulty):
        super(WealthGoblin, self).__init__(coord_x, coord_y, difficulty)
        self._coins = random.randint(10, 300)
        self._probability = round(((400 - self._coins) * self._difficulty) / 4)

    def give_coin(self, hero):
        probability_list = range(1, self._probability + 1)  # list of numbers stating the probability
        if random.randint(1, 100) in probability_list:  # random number N = <1;100> check if is in probability_list
            hero.set_coins(hero.get_coins() + self._coins)
            print("You have received", self._coins, "coins, your have now", hero.get_coins(), "coins")
        else:
            print("You are unlucky, the goblin did not give you any coin.")


class HealthGoblin(Goblin):
    def __init__(self, coord_x, coord_y, difficulty):
        super(HealthGoblin, self).__init__(coord_x, coord_y, difficulty)
        self._health = random.randint(1, 50)
        self._probability = round((100 - self._health) * self._difficulty)

    def give_health(self, hero):
        probability_list = range(1, self._probability + 1)  # list of numbers stating the probability
        if random.randint(1, 100) in probability_list:  # random number N = <1;100> check if is in probability_list
            hero.set_health(hero.get_health() + self._health)
            print("The goblin has healed by", self._health, "health, your have now", hero.get_health(), "health")
        else:
            print("You are unlucky, the goblin did not heal you.")


class GamerGoblin(Goblin):
    def __init__(self, coord_x, coord_y, difficulty):
        super(GamerGoblin, self).__init__(coord_x, coord_y, difficulty)
        self._health = random.randint(1, 50)
        self._coins = random.randint(10, 300)

    def play(self, hero):
        if rock_paper_scissors():
            print("You lost, you don't get anything from this goblin.")
        else:
            hero.set_coins(hero.get_coins() + self._coins)
            hero.set_health(hero.get_health() + self._health)
            print("You received", self._coins, "coins and", self._health, "health, you have", hero.get_coins(),
                  "coins and", hero.get_health(), "health")
