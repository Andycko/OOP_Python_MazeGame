#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0

import random

from src.functions.helpers import rock_paper_scissors


class Monster:
    all_monsters = []  # All Monster objects are stored here
    visited_monsters = []  # All already visited Monster objects are stored here

    def __init__(self, coord_x, coord_y, difficulty):
        self._coordX = coord_x
        self._coordY = coord_y
        if difficulty == "easy":
            self._difficulty = 0.6
        elif difficulty == "medium":
            self._difficulty = 0.9
        else:
            self._difficulty = 1.2
        Monster.all_monsters.append(self)

    def get_coordinates(self):
        """ Coordinates getter method """
        return self._coordX, self._coordY

    def visit(self, hero):
        """ Visit method for hero to visit the monster and receive gem """
        if self not in Monster.visited_monsters:
            Monster.visited_monsters.append(self)
            hero.give_gem()
        else:
            print("You have already took your gem from this monster, try looking somewhere else.\n")


class FighterMonster(Monster):
    def __init__(self, coord_x, coord_y, difficulty):
        super(FighterMonster, self).__init__(coord_x, coord_y, difficulty)
        self._damage = random.randint(1, 50)
        self._probability = round((100 - self._damage) * self._difficulty)

    def fight(self, hero):
        """ Main interaction method of this Goblin """
        print("You have met a Fighter monster with", self._damage, "damage and", str(self._probability) +
              "% probability to hit you")
        probability_list = range(1, self._probability + 1)  # list of numbers stating the probability
        if random.randint(1, 100) in probability_list:  # random number N = <1;100> check if is in probability_list
            hero.set_health(hero.get_health() - self._damage)
            print("You have suffered", self._damage, "damage, your life is now", hero.get_health(), "\n")
        else:
            print("You are lucky, the monster did not hit you and you can continue.\n")
        self.visit(hero)


class ThiefMonster(Monster):
    def __init__(self, coord_x, coord_y, difficulty):
        super(ThiefMonster, self).__init__(coord_x, coord_y, difficulty)
        self._steal = random.randint(20, 400)
        self._probability = round(((500 - self._steal) * self._difficulty) / 5)

    def steal(self, hero):
        """ Main interaction method of this Goblin """
        print("You have met a Thief monster with", self._steal, "coin steal and", str(self._probability) +
              "% probability to steal from you")
        probability_list = range(1, self._probability + 1)  # list of numbers stating the probability
        if random.randint(1, 100) in probability_list:  # random number N = <1;100> check if is in probability_list
            hero.set_coins(hero.get_coins() - self._steal)
            print("You have lost", self._steal, "coins, you have", hero.get_coins(), "coins.\n")
        else:
            print("You are lucky, the monster did not steal anything from you and you can continue.\n")
        self.visit(hero)


class GamerMonster(Monster):
    """ Main interaction method of this Goblin """
    def __init__(self, coord_x, coord_y, difficulty):
        super(GamerMonster, self).__init__(coord_x, coord_y, difficulty)
        self._damage = random.randint(1, 50)
        self._steal = random.randint(10, 300)

    def play(self, hero):
        print("You have met a Gamer monster with", self._damage, "damage and", self._steal, "coin steal")
        if rock_paper_scissors():
            hero.set_coins(hero.get_coins() - self._steal)
            hero.set_health(hero.get_health() - self._damage)
            print("You have lost", self._steal, "coins and", self._damage, "health, you have", hero.get_coins(),
                  "coins and", hero.get_health(), "health.\n")
        else:
            print("You defeated the monster, you may continue your journey.\n")
        self.visit(hero)
