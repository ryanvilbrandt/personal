from collections import defaultdict
from enum import Enum
from math import ceil

ROUND_FACTORIES = False


class FactorySpeed(Enum):
    ASSEMBLER = 0.75
    SMELTER = 2
    PULVERIZER = 2
    CHEMICAL_PLANT = 1


class Item:

    def __init__(self, name, crafting_time=1.0, num_created=1, recipe=None, factory_speed=FactorySpeed.ASSEMBLER):
        self.name = name
        self.crafting_time = crafting_time
        self.num_created = num_created
        self.recipe = recipe
        self.is_raw_material = recipe is None
        self.num_per_second = 0.0 if self.is_raw_material else (num_created * factory_speed.value / crafting_time)

    def analyze(self, factories=None, num_per_second_needed=None, ignore=None):
        if num_per_second_needed is None:
            num_per_second_needed = factories * self.num_per_second
        if ignore is None:
            ignore = []
        d = self.recurse(num_per_second_needed, ignore)
        ingredients = []
        raw_materials = []
        max_name_length = 0
        print("")
        for item, amount in d.items():
            if item == self:
                self.print(amount)
            elif item.is_raw_material:
                raw_materials.append((item, amount))
            else:
                max_name_length = max(max_name_length, len(item.name))
                ingredients.append((item, amount))
        print("")
        for item, amount in ingredients:
            item.print(amount, max_name_length)
        print("")
        for item, amount in raw_materials:
            item.print(round(amount, 5))

    def recurse(self, num_per_second_needed, ignore_items):
        if self in ignore_items:
            return {}
        d = defaultdict(float)
        d[self] = float(num_per_second_needed)
        if self.is_raw_material:
            return d
        for item, n in self.recipe.items():
            item_d = item.recurse(num_per_second_needed * n, ignore_items)
            # print(f"{self.name}: {self.to_dict(item_d)}")
            for child_item, child_npsn in item_d.items():
                d[child_item] += child_npsn / self.num_created
            # print(f"{self.name}: {self.to_dict(item_d)}")
        return d

    @staticmethod
    def to_dict(d):
        return {k.name: v for k, v in d.items()}

    def print(self, amount, max_name_length=0, indent=0):
        if self.is_raw_material:
            print(f"{self.name}: {amount}/s")
        else:
            factories = amount / self.num_per_second
            if ROUND_FACTORIES:
                factories = ceil(factories)
            print(("{}{:<" + str(max_name_length) + "}   {} factories ({}/s)").format(
                "  " * indent, self.name, round(factories, 3), round(amount, 3)
            ))


# Raw goods
COAL = Item("Coal")
WATER = Item("Water")
STONE = Item("Stone")

SAND = Item("Sand", 0.5, 3, {STONE: 1}, factory_speed=FactorySpeed.PULVERIZER)

# Smelted goods
STONE_BRICK = Item("Stone brick", factory_speed=FactorySpeed.SMELTER)
IRON_PLATE = Item("Iron plate", factory_speed=FactorySpeed.SMELTER)
COPPER_PLATE = Item("Copper plate", factory_speed=FactorySpeed.SMELTER)
STEEL_PLATE = Item("Steel plate", factory_speed=FactorySpeed.SMELTER)
GLASS = Item("Glass", 4, 1, {SAND: 4}, factory_speed=FactorySpeed.SMELTER)

# Oil goods
PETROLEUM_GAS = Item("Petroleum gas")
LUBRICANT = Item("Lubricant")
SULFUR = Item("Sulfur", 1, 2, {WATER: 30, PETROLEUM_GAS: 30}, factory_speed=FactorySpeed.CHEMICAL_PLANT)
SULFURIC_ACID = Item("Sulfuric acid", 1, 50, {IRON_PLATE: 1, SULFUR: 5, WATER: 100}, factory_speed=FactorySpeed.CHEMICAL_PLANT)

# Processed goods
IRON_STICK = Item("Iron stick", 0.5, 2, {IRON_PLATE: 1})
IRON_GEAR = Item("Iron gear wheel", 0.5, 1, {IRON_PLATE: 2})
COPPER_CABLE = Item("Copper cable", 0.5, 2, {COPPER_PLATE: 1})
STONE_TABLET = Item("Stone tablet", 0.5, 4, {STONE_BRICK: 1})
PLASTIC_BAR = Item("Plastic bar", 1, 2, {COAL: 1, PETROLEUM_GAS: 20})

# Factory Equipment
PIPE = Item("Pipe", 0.5, 1, {IRON_PLATE: 1})

# Manufactured goods
ELECTRONIC_CIRCUIT = Item("Electronic circuit", 0.5, 1, {COPPER_CABLE: 3, STONE_TABLET: 1})
MOTOR = Item("Motor", 0.6, 1, {IRON_GEAR: 1, IRON_PLATE: 1})
ELECTRIC_MOTOR = Item("Electric motor", 0.8, 1, {MOTOR: 1, COPPER_CABLE: 6})
ADVANCED_CIRCUIT = Item("Advanced circuit", 6, 1, {COPPER_CABLE: 4, ELECTRONIC_CIRCUIT: 2, PLASTIC_BAR: 2})
ENGINE_UNIT = Item("Engine unit", 10, 1, {IRON_GEAR: 2, MOTOR: 1, PIPE: 2, STEEL_PLATE: 2})
ELECTRIC_ENGINE = Item("Electric engine unit", 10, 1, {ELECTRONIC_CIRCUIT: 1, ELECTRIC_MOTOR: 1, ENGINE_UNIT: 1, LUBRICANT: 40})
BATTERY = Item("Battery", 4, 1, {IRON_PLATE: 1, COPPER_PLATE: 1, SULFURIC_ACID: 20}, factory_speed=FactorySpeed.CHEMICAL_PLANT)

# Factory equipment (continued)
TRANSPORT_BELT = Item("Transport belt", 0.5, 2, {MOTOR: 1, IRON_PLATE: 1})
BURNER_INSERTER = Item("Burner inserter", 0.5, 1, {IRON_STICK: 2, MOTOR: 1})
ELECTRIC_INSERTER = Item("Inserter", 0.5, 1, {ELECTRIC_MOTOR: 1, BURNER_INSERTER: 1})
FAST_INSERTER = Item("Fast inserter", 0.5, 1, {ELECTRONIC_CIRCUIT: 2, ELECTRIC_INSERTER: 1, IRON_PLATE: 2})
SOLAR_PANEL = Item("Solar panel", 10, 1, {ELECTRONIC_CIRCUIT: 15, GLASS: 4, COPPER_PLATE: 4, STEEL_PLATE: 4})
ACCUMULATOR = Item("Accumulator", 10, 1, {BATTERY: 5, IRON_PLATE: 2})

# Robots
FLYING_ROBOT_FRAME = Item("Flying robot frame", 20, 1, {ELECTRONIC_CIRCUIT: 4, ELECTRIC_ENGINE: 4, BATTERY: 4, STEEL_PLATE: 4})

# Military
FIREARM_MAGAZINE = Item("Firearm magazine", 1, 1, {IRON_PLATE: 4})
PIERCING_MAGAZINE = Item("Piercing rounds magazine", 3, 1, {COPPER_PLATE: 5, STEEL_PLATE: 1, FIREARM_MAGAZINE: 1})
GRENADE = Item("Grenade", 8, 1, {IRON_PLATE: 5, COAL: 10})
STONE_WALL = Item("Stone wall", 0.5, 1, {STONE_BRICK: 5})
LASER_TURRET = Item("Laser turret", 20, 1, {ELECTRONIC_CIRCUIT: 20, ELECTRIC_MOTOR: 5, BATTERY: 12, GLASS: 20, STEEL_PLATE: 20})

# SCIENCE!
AUTOMATION_SCIENCE = Item("Automation science pack", 5, 1, {IRON_GEAR: 1, COPPER_PLATE: 1})
LOGISTIC_SCIENCE = Item("Logistic science pack", 10, 2, {TRANSPORT_BELT: 2, ELECTRIC_INSERTER: 1})
MILITARY_SCIENCE = Item("Military science pack", 10, 2, {PIERCING_MAGAZINE: 1, GRENADE: 1, STONE_WALL: 2})
CHEMICAL_SCIENCE = Item("Chemical science pack", 24, 2, {ADVANCED_CIRCUIT: 3, ENGINE_UNIT: 2, SULFUR: 1})
ALL_SCIENCE = Item("All science packs", 1, 1, {AUTOMATION_SCIENCE: 1, LOGISTIC_SCIENCE: 1, MILITARY_SCIENCE: 1, 
                                               CHEMICAL_SCIENCE: 1})

# MOTOR.analyze(5)
# ELECTRONIC_CIRCUIT.analyze(4)
# FAST_INSERTER.analyze(0.5)

# ELECTRONIC_CIRCUIT.analyze(4)
# ADVANCED_CIRCUIT.analyze(6, ignore=[ELECTRONIC_CIRCUIT])

# AUTOMATION_SCIENCE.analyze(num_per_second_needed=1)
# LOGISTIC_SCIENCE.analyze(num_per_second_needed=1)
# MILITARY_SCIENCE.analyze(num_per_second_needed=1)
# CHEMICAL_SCIENCE.analyze(num_per_second_needed=1)
ALL_SCIENCE.analyze(1)

# ENGINE_UNIT.analyze(10)

# TRANSPORT_BELT.analyze(1)

# FIREARM_MAGAZINE.analyze(num_per_second_needed=3)
# PIERCING_MAGAZINE.analyze(num_per_second_needed=3)

# FLYING_ROBOT_FRAME.analyze(5)
# SOLAR_PANEL.analyze(8)
# ACCUMULATOR.analyze(8)
# LASER_TURRET.analyze(4, ignore=[SULFURIC_ACID, GLASS, BATTERY, ELECTRONIC_CIRCUIT])

# SULFURIC_ACID.analyze(3)

# FLYING_ROBOT_FRAME.analyze(1, ignore=[SULFURIC_ACID, ELECTRIC_MOTOR, ELECTRONIC_CIRCUIT, ENGINE_UNIT])
