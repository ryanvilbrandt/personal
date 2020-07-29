from collections import defaultdict


class Item:

    def __init__(self, name, crafting_time=0.0, num_created=1, recipe=None):
        self.name = name
        self.crafting_time = crafting_time
        self.num_created = num_created
        self.recipe = recipe

    def analyze(self, num_factories):
        if self.crafting_time == 0:
            return {self.name: 1}
        ingredients = defaultdict(int)
        for parent_item, parent_n in self.recipe.items():
            for item, n in parent_item.analyze():




IRON_PLATE = Item("Iron plate")
COPPER_PLATE = Item("Copper plate")
IRON_STICK = Item("Iron stick", 0.5, 2, {IRON_PLATE: 1})
IRON_GEAR = Item("Iron gear wheel", 0.5, 1, {IRON_PLATE: 2})
COPPER_CABLE = Item("Copper cable", 0.5, 2, {COPPER_PLATE: 1})
MOTOR = Item("Motor", 0.6, 1, {IRON_GEAR: 1, IRON_PLATE: 1})
