from collections import defaultdict
from math import ceil

ROUND_FACTORIES = True


class Pair:

    def __init__(self, num_per_second, factories_needed):
        self.num_per_second = num_per_second
        self.factories_needed = factories_needed

    def __add__(self, other):
        if not isinstance(other, Pair):
            raise TypeError("Can only add Pair to Pair")
        return Pair(self.num_per_second + other.num_per_second, self.factories_needed + other.factories_needed)


class Item:

    def __init__(self, name, crafting_time=1.0, num_created=1, recipe=None):
        self.name = name
        self.crafting_time = crafting_time
        self.num_created = num_created
        self.recipe = recipe
        self.num_per_second = 0.0 if recipe is None else num_created / crafting_time
        self.is_raw_material = recipe is None

    def analyze(self, factories=None, num_per_second_needed=None):
        if num_per_second_needed is None:
            num_per_second_needed = factories / self.crafting_time
        if factories is None:
            factories = ceil(num_per_second_needed * self.crafting_time)
        d = self.recurse(num_per_second_needed)
        ingredients = []
        raw_materials = []
        max_name_length = 0
        for item, amount in d.items():
            if item == self:
                self.print(amount)
            elif item.is_raw_material:
                raw_materials.append((item, amount))
            else:
                max_name_length = max(max_name_length, len(item.name))
                ingredients.append((item, amount))
        print("")
        # print(max_name_length)
        # print(len("Electronic circuit"))
        for item, amount in ingredients:
            item.print(amount, max_name_length)
        print("")
        for item, amount in raw_materials:
            item.print(amount)

    def recurse(self, num_per_second_needed):
        d = defaultdict(int)
        d[self] = float(num_per_second_needed)
        if self.is_raw_material:
            return d
        for item, n in self.recipe.items():
            item_d = item.recurse(num_per_second_needed * n)
            # print(f"{self.name}: {self.to_dict(item_d)}")
            for child_item, child_npsn in item_d.items():
                d[child_item] += child_npsn / self.num_created
            # print(f"{self.name}: {self.to_dict(item_d)}")
        return d

    @staticmethod
    def to_dict(d):
        return {k.name: v for k, v in d.items()}

    def print(self, amount, max_name_length=None):
        if self.is_raw_material:
            print(f"{self.name}: {amount}/s")
        else:
            factories = amount / self.num_per_second
            if ROUND_FACTORIES:
                factories = ceil(factories)
            fmt = ("{:<" + str(max_name_length + 2) + "} {} factories ({}/s)") if max_name_length else "{}: {} factories ({}/s)"
            # print(fmt)
            print(fmt.format(self.name, factories, amount))


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
TRANSPORT_BELT = Item("Transport belt", 0.5, 2, {MOTOR: 1, IRON_PLATE: 1})
BURNER_INSERTER = Item("Burner inserter", 0.5, 1, {IRON_STICK: 2, MOTOR: 1})
ELECTRIC_INSERTER = Item("Inserter", 0.5, 1, {ELECTRIC_MOTOR: 1, BURNER_INSERTER: 1})
FAST_INSERTER = Item("Fast inserter", 0.5, 1, {ELECTRONIC_CIRCUIT: 2, ELECTRIC_INSERTER: 1, IRON_PLATE: 2})

# SCIENCE!

AUTOMATION_SCIENCE = Item("Automation science pack", 5, 1, {IRON_GEAR: 1, COPPER_PLATE: 1})
LOGISTIC_SCIENCE = Item("Logistic science pack", 10, 2, {TRANSPORT_BELT: 2, ELECTRIC_INSERTER: 1})

# MOTOR.analyze(5)
# ELECTRONIC_CIRCUIT.analyze(5)
# FAST_INSERTER.analyze(1)

# AUTOMATION_SCIENCE.analyze(5)
# LOGISTIC_SCIENCE.analyze(10)
TRANSPORT_BELT.analyze(1)
