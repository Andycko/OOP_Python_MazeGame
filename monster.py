#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0

import random
from helpers import rock_paper_scissors


class Monster:
    """define your monster class here"""
    def __init__(self, coord_x, coord_y):
        self._coordX = coord_x
        self._coordY = coord_y

    def get_coordinates(self):
        return self._coordX, self._coordY

    def disappear(self):
        return False


class FighterMonster(Monster):
    def __init__(self, coord_x, coord_y):
        super(FighterMonster, self).__init__(coord_x, coord_y)
        self._damage = random.randint(1, 50)
        self._probability = round((100 - self._damage) * random.uniform(0.6, 1.2))

    def fight(self, hero):
        probability_list = range(1, self._probability + 1)    # list of numbers stating the probability
        if random.randint(1, 100) in probability_list:   # random number N = <1;100> check if is in probability_list
            hero.set_health(hero.get_health() - self._damage)
            print("You have suffered", self._damage, "damage, your life is now", hero.get_health())
            self.disappear()
        else:
            print("You are lucky, the monster did not hit you and you can continue")
            self.disappear()


class ThiefMonster(Monster):
    def __init__(self, coord_x, coord_y):
        super(ThiefMonster, self).__init__(coord_x, coord_y)
        self._steal = random.randint(20, 400)
        self._probability = round(((500 - self._steal) * random.uniform(0.6, 1.2)) / 5)

    def steal(self, hero):
        probability_list = range(1, self._probability + 1)    # list of numbers stating the probability
        if random.randint(1, 100) in probability_list:   # random number N = <1;100> check if is in probability_list
            hero.set_coins(hero.get_coins() - self._steal)
            print("You have lost", self._steal, "coins, you have", hero.get_coins(), "coins")
            self.disappear()
        else:
            print("You are lucky, the monster did not steal anything from you and you can continue")
            self.disappear()


class GamerMonster(Monster):
    def __init__(self, coord_x, coord_y):
        super(GamerMonster, self).__init__(coord_x, coord_y)
        self._damage = random.randint(1, 50)
        self._steal = random.randint(10, 300)

    def play(self, hero):
        if rock_paper_scissors():
            hero.set_coins(hero.get_coins() - self._steal)
            hero.set_health(hero.get_health() - self._damage)
            print("You have lost", self._steal, "coins and", self._damage, "health, you have", hero.get_coins(), "coins and", hero.get_health(), "health")
        else:
            print("You defeated the monster, you may continue your journey.")
            self.disappear()
