from collections import defaultdict
from math import ceil


class Item:

    def __init__(self, name, crafting_time=0.0, num_created=1, recipe=None):
        self.name = name
        self.crafting_time = crafting_time
        self.num_created = num_created
        self.num_per_second = 0 if crafting_time == 0 else num_created / crafting_time
        self.recipe = recipe

    def analyze(self, num_per_second=1.0):
        if self.num_per_second == 0:
            print("{}/s {} needed".format(num_per_second, self.name))
            return
        print("{}/s {} needed ({} factories)".format(num_per_second, self.name, ceil(num_per_second / self.num_per_second)))
        for item, n in self.recipe.items():
            item.analyze(self.num_per_second * n)

# Smelted goods
STONE_BRICK = Item("Stone brick")
IRON_PLATE = Item("Iron plate")
COPPER_PLATE = Item("Copper plate")

# Processed goods
IRON_STICK = Item("Iron stick", 0.5, 2, {IRON_PLATE: 1})
IRON_GEAR = Item("Iron gear wheel", 0.5, 1, {IRON_PLATE: 2})
COPPER_CABLE = Item("Copper cable", 0.5, 2, {COPPER_PLATE: 1})
STONE_TABLET = Item("Stone tablet", 0.5, 4, {STONE_BRICK: 1})

# Manufactured goods
ELECTRONIC_CIRCUIT = Item("Electronic circuit", 0.5, 1, {COPPER_CABLE: 3, STONE_TABLET: 1})
MOTOR = Item("Motor", 0.6, 1, {IRON_GEAR: 1, IRON_PLATE: 1})
ELECTRIC_MOTOR = Item("Electric motor", 0.8, 1, {MOTOR: 1, COPPER_CABLE: 6})

# Factory equipment
BURNER_INSERTER = Item("Burner inserter", 0.5, 1, {IRON_STICK: 2, MOTOR: 1})
ELECTRIC_INSERTER = Item("Inserter", 0.5, 1, {ELECTRIC_MOTOR: 1, BURNER_INSERTER: 1})
FAST_INSERTER = Item("Fast inserter", 0.5, 1, {ELECTRONIC_CIRCUIT: 2, ELECTRIC_INSERTER: 1, IRON_PLATE: 2})


ELECTRIC_MOTOR.analyze(0.8)
