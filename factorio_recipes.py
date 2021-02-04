from collections import defaultdict
from enum import Enum
from math import ceil

ROUND_FACTORIES = False

# Machine speeds
S_ASSEMBLER = 1.25
S_MANUFACTORY = 10
S_SMELTER = 2
S_PULVERISER = 2
S_CHEMICAL_PLANT = 1
S_FUEL_REFINERY = 1
S_DECONTAMINATION_FACILITY = 2
S_SUPERCOMPUTER = 1
S_RADIATOR = 1


class Item:

    def __init__(self, name, crafting_time=1.0, num_created=1, recipe=None, factory_speed=S_ASSEMBLER):
        self.name = name
        self.crafting_time = crafting_time
        self.num_created = num_created
        self.recipe = recipe
        self.is_raw_material = recipe is None
        self.num_per_second = 0.0 if self.is_raw_material else (num_created * factory_speed / crafting_time)

    def analyze(self, factories=None, num_per_second_needed=None, ignore=None):
        print("=======================================")
        if num_per_second_needed is None:
            num_per_second_needed = factories * self.num_per_second
        if ignore is None:
            ignore = []
        d = self.analyze_recurse(num_per_second_needed, ignore)
        ingredients = []
        raw_materials = []
        max_name_length = 0
        print("")
        for item, amount in d.items():
            if item == self:
                self.print(amount)
            elif item.is_raw_material or item in ignore:
                raw_materials.append((item, amount))
            else:
                max_name_length = max(max_name_length, len(item.name))
                ingredients.append((item, amount))
        if ingredients:
            print("")
            for item, amount in ingredients:
                item.print(amount, max_name_length)
        print("")
        for item, amount in raw_materials:
            item.print(round(amount, 5), is_raw_material=True)
        print("")

    def analyze_recurse(self, num_per_second_needed, ignore_items, indent=0):
        print("{}{}".format(" " * indent, self.name))
        d = defaultdict(float)
        d[self] = float(num_per_second_needed)
        if self.is_raw_material or self in ignore_items:
            return d
        for item, n in self.recipe.items():
            item_d = item.analyze_recurse(num_per_second_needed * n, ignore_items, indent + 1)
            # print(f"{self.name}: {self.to_dict(item_d)}")
            for child_item, child_npsn in item_d.items():
                d[child_item] += child_npsn / self.num_created
            # print(f"{self.name}: {self.to_dict(item_d)}")
        return d

    def count(self, total_needed, ignore=None):
        print("=======================================")
        print("{}x {}".format(round(total_needed, 2), self.name))
        print("")
        if ignore is None:
            ignore = []
        count_d = self.count_recurse(total_needed, ignore)
        print("")
        for item, n in count_d.items():
            print("{}x {}".format(round(n, 2), item.name))

    def count_recurse(self, total_needed, ignore_items, indent=0):
        print("{}{}".format(" " * indent, self.name))
        if self.is_raw_material or self in ignore_items:
            return {self: total_needed}
        count_d = defaultdict(int)
        for item, n in self.recipe.items():
            d = item.count_recurse(total_needed * n, ignore_items, indent + 1)
            for child_item, child_n in d.items():
                count_d[child_item] += child_n / self.num_created
        return count_d

    @staticmethod
    def to_dict(d):
        return {k.name: v for k, v in d.items()}

    def print(self, amount, max_name_length=0, indent=0, is_raw_material=False):
        if is_raw_material:
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
VULCANITE = Item("Vulcanite")

SAND = Item("Sand", 0.5, 3, {STONE: 1}, S_PULVERISER)

# Smelted goods
STONE_BRICK = Item("Stone brick", factory_speed=S_SMELTER)
IRON_PLATE = Item("Iron plate", factory_speed=S_SMELTER)
COPPER_PLATE = Item("Copper plate", factory_speed=S_SMELTER)
STEEL_PLATE = Item("Steel plate", factory_speed=S_SMELTER)
GLASS = Item("Glass", 4, 1, {SAND: 4}, factory_speed=S_SMELTER)
CRUSHED_VULCANITE = Item("Crushed vulcanite", 0.5, 1, {VULCANITE: 2}, S_PULVERISER)
WASHED_VULCANITE = Item("Washed vulcanite", 1, 1, {CRUSHED_VULCANITE: 2, WATER: 6}, S_CHEMICAL_PLANT)
VULCANITE_BLOCK = Item("Vulcanite block", 1, 1, {WASHED_VULCANITE: 1})

# Oil goods
PETROLEUM_GAS = Item("Petroleum gas")
LIGHT_OIL = Item("Light oil")
HEAVY_OIL = Item("Heavy oil")
LUBRICANT = Item("Lubricant", 1, 10, {HEAVY_OIL: 10}, S_CHEMICAL_PLANT)
SULFUR = Item("Sulfur", 1, 2, {WATER: 30, PETROLEUM_GAS: 30}, S_CHEMICAL_PLANT)
SULFURIC_ACID = Item("Sulfuric acid", 1, 50, {IRON_PLATE: 1, SULFUR: 5, WATER: 100}, S_CHEMICAL_PLANT)
EXPLOSIVES = Item("Explosives", 4, 2, {COAL: 1, SULFUR: 1, WATER: 10}, S_CHEMICAL_PLANT)
SOLID_FUEL = Item("Solid fuel", 0.5, 1, {LIGHT_OIL: 10}, S_FUEL_REFINERY)

# Processed goods
IRON_STICK = Item("Iron stick", 0.5, 2, {IRON_PLATE: 1})
IRON_GEAR = Item("Iron gear wheel", 0.5, 1, {IRON_PLATE: 2})
COPPER_CABLE = Item("Copper cable", 0.5, 2, {COPPER_PLATE: 1})
STONE_TABLET = Item("Stone tablet", 0.5, 4, {STONE_BRICK: 1})
PLASTIC_BAR = Item("Plastic bar", 1, 2, {COAL: 1, PETROLEUM_GAS: 20})

# Factory Equipment
PIPE = Item("Pipe", 0.5, 1, {IRON_PLATE: 1})
EMPTY_BARREL = Item("Empty barrel", 1, 1, {STEEL_PLATE: 1})

# Manufactured goods
ELECTRONIC_CIRCUIT = Item("Electronic circuit", 0.5, 1, {COPPER_CABLE: 3, STONE_TABLET: 1})
MOTOR = Item("Motor", 0.6, 1, {IRON_GEAR: 1, IRON_PLATE: 1})
ELECTRIC_MOTOR = Item("Electric motor", 0.8, 1, {MOTOR: 1, COPPER_CABLE: 6})
ADVANCED_CIRCUIT = Item("Advanced circuit", 6, 1, {COPPER_CABLE: 4, ELECTRONIC_CIRCUIT: 2, PLASTIC_BAR: 2})
ENGINE_UNIT = Item("Engine unit", 10, 1, {IRON_GEAR: 2, MOTOR: 1, PIPE: 2, STEEL_PLATE: 2})
ELECTRIC_ENGINE = Item("Electric engine unit", 10, 1, {ELECTRONIC_CIRCUIT: 1, ELECTRIC_MOTOR: 1, ENGINE_UNIT: 1, LUBRICANT: 40})
BATTERY = Item("Battery", 4, 1, {IRON_PLATE: 1, COPPER_PLATE: 1, SULFURIC_ACID: 20}, S_CHEMICAL_PLANT)
HEAT_SHIELDING = Item("Heat shielding", 10, 1, {STONE_TABLET: 20, STEEL_PLATE: 2, SULFUR: 8})
PROCESSING_UNIT = Item("Processing unit", 10, 1, {ELECTRONIC_CIRCUIT: 20, ADVANCED_CIRCUIT: 2, SULFURIC_ACID: 5})
LOW_DENSITY_STRUCTURE = Item("Low density structure", 20, 1, {GLASS: 10, COPPER_PLATE: 10, STEEL_PLATE: 5, PLASTIC_BAR: 10})

# Factory equipment (continued)
TRANSPORT_BELT = Item("Transport belt", 0.5, 2, {MOTOR: 1, IRON_PLATE: 1})
BURNER_INSERTER = Item("Burner inserter", 0.5, 1, {IRON_STICK: 2, MOTOR: 1})
ELECTRIC_INSERTER = Item("Inserter", 0.5, 1, {ELECTRIC_MOTOR: 1, BURNER_INSERTER: 1})
FAST_INSERTER = Item("Fast inserter", 0.5, 1, {ELECTRONIC_CIRCUIT: 2, ELECTRIC_INSERTER: 1, IRON_PLATE: 2})
SOLAR_PANEL = Item("Solar panel", 10, 1, {ELECTRONIC_CIRCUIT: 15, GLASS: 4, COPPER_PLATE: 4, STEEL_PLATE: 4})
ACCUMULATOR = Item("Accumulator", 10, 1, {BATTERY: 5, IRON_PLATE: 2})
RAIL = Item("Rail", 0.5, 2, {IRON_STICK: 1, STEEL_PLATE: 1, STONE: 1})
STONE_FURNACE = Item("Stone furnace", 0.5, 1, {STONE: 5})
STEEL_FURNACE = Item("Steel furnace", 3, 1, {STONE_BRICK: 6, STONE_FURNACE: 1, STEEL_PLATE: 6})
ELECTRIC_FURNACE = Item("Electric furnace", 5, 1, {ADVANCED_CIRCUIT: 5, HEAT_SHIELDING: 2, STEEL_FURNACE: 1, STEEL_PLATE: 5})
PRODUCTIVITY_MODULE = Item("Productivity module", 2, 1, {ELECTRONIC_CIRCUIT: 2, ADVANCED_CIRCUIT: 1})
RADAR = Item("Radar", 0.5, 1, {ELECTRONIC_CIRCUIT: 8, ELECTRIC_MOTOR: 4, STONE_BRICK: 4, IRON_PLATE: 20})

# Machines


# Robots
FLYING_ROBOT_FRAME = Item("Flying robot frame", 20, 1, {ELECTRONIC_CIRCUIT: 4, ELECTRIC_ENGINE: 4, BATTERY: 4, STEEL_PLATE: 4})

# Military
FIREARM_MAGAZINE = Item("Firearm magazine", 1, 1, {IRON_PLATE: 4})
PIERCING_MAGAZINE = Item("Piercing rounds magazine", 3, 1, {COPPER_PLATE: 5, STEEL_PLATE: 1, FIREARM_MAGAZINE: 1})
GRENADE = Item("Grenade", 8, 1, {IRON_PLATE: 5, COAL: 10})
STONE_WALL = Item("Stone wall", 0.5, 1, {STONE_BRICK: 5})
LASER_TURRET = Item("Laser turret", 20, 1, {ELECTRONIC_CIRCUIT: 20, ELECTRIC_MOTOR: 5, BATTERY: 12, GLASS: 20, STEEL_PLATE: 20})
CANNON_SHELL = Item("Cannon shell", 8, 1, {EXPLOSIVES: 1, STEEL_PLATE: 2, PLASTIC_BAR: 2})
EXPLOSIVE_CANNON_SHELL = Item("Explosive cannon shell", 8, 1, {EXPLOSIVES: 2, STEEL_PLATE: 2, PLASTIC_BAR: 2})
ARTILLERY_SHELL = Item("Artillery shell", 15, 1, {EXPLOSIVES: 8, EXPLOSIVE_CANNON_SHELL: 4, RADAR: 1})

# Rocket stuff
ROCKET_CONTROL_UNIT = Item("Rocket control unit", 30, 1, {ADVANCED_CIRCUIT: 5, PROCESSING_UNIT: 1, BATTERY: 5, GLASS: 5, IRON_PLATE: 5})
SOLID_ROCKET_FUEL = Item("Solid rocket fuel", 1, 1, {VULCANITE_BLOCK: 8}, S_FUEL_REFINERY)
# SOLID_ROCKET_FUEL = Item("Solid rocket fuel", 1, 1, {SOLID_FUEL: 10, LIGHT_OIL: 10}, FUEL_REFINERY)
ROCKET_PART = Item("Rocket part", 3, 1, {HEAT_SHIELDING: 5, LOW_DENSITY_STRUCTURE: 5, ROCKET_CONTROL_UNIT: 5, SOLID_ROCKET_FUEL: 10}, 
                   factory_speed=0.2)

# Spaaaaace
SPACE_PLATFORM = Item("Space platform scaffold", 10, 1, {HEAT_SHIELDING: 1, LOW_DENSITY_STRUCTURE: 1, STEEL_PLATE: 1})
COSMIC_WATER = Item("Cosmic water", 1, 10, {WATER: 99, LUBRICANT: 1}, factory_speed=S_DECONTAMINATION_FACILITY)
CHEMICAL_GEL = Item("Chemical gel", 10, 20, {COSMIC_WATER: 10, PETROLEUM_GAS: 100}, factory_speed=S_MANUFACTORY)
THERMOFLUID = Item("Thermofluid 25o", 5, 10, {IRON_PLATE: 1, COPPER_PLATE: 2, SULFUR: 1, COSMIC_WATER: 1, HEAVY_OIL: 20},
                   factory_speed=S_MANUFACTORY)
COOL_THERMOFLUID = Item("Cool thermofluid -10o", 10, 49, {THERMOFLUID: 50}, factory_speed=S_RADIATOR)
ROUGH_DS_SUBSTRATE = Item("Rough data storage substrate", 5, 1, {GLASS: 2, IRON_PLATE: 4})
# POLISHED_DS_SUBSTRATE = Item("Polished data storage substrate", 2.5, 1, {ROUGH_DS_SUBSTRATE: 1, COSMIC_WATER: 5}, 
#                              factory_speed=DECONTAMINATION_FACILITY)
POLISHED_DS_SUBSTRATE = Item("Polished data storage substrate", 2.5, 1, {ROUGH_DS_SUBSTRATE: 1, COSMIC_WATER: 5},
                             factory_speed=S_DECONTAMINATION_FACILITY)
BLANK_DATA_CARD = Item("Blank data card", 10, 1, {ADVANCED_CIRCUIT: 3, COPPER_PLATE: 6, POLISHED_DS_SUBSTRATE: 1},
                       factory_speed=S_MANUFACTORY)
MACHINE_LEARNING_DATA = Item("Machine learning data", 10, 1, {ELECTRONIC_CIRCUIT: 1, BLANK_DATA_CARD: 1, COOL_THERMOFLUID: 1},
                             factory_speed=S_SUPERCOMPUTER)

# SCIENCE!
AUTOMATION_SCIENCE = Item("Automation science pack", 5, 1, {IRON_GEAR: 1, COPPER_PLATE: 1})
LOGISTIC_SCIENCE = Item("Logistic science pack", 10, 2, {TRANSPORT_BELT: 2, ELECTRIC_INSERTER: 1})
MILITARY_SCIENCE = Item("Military science pack", 10, 2, {PIERCING_MAGAZINE: 1, GRENADE: 1, STONE_WALL: 2})
CHEMICAL_SCIENCE = Item("Chemical science pack", 24, 2, {ADVANCED_CIRCUIT: 3, ENGINE_UNIT: 2, SULFUR: 1})
PRODUCTION_SCIENCE = Item("Production science pack", 21, 3, {RAIL: 30, ELECTRIC_FURNACE: 1, PRODUCTIVITY_MODULE: 1})
UTILITY_SCIENCE = Item("Utility science pack", 35, 5, {PROCESSING_UNIT: 3, FLYING_ROBOT_FRAME: 1, LOW_DENSITY_STRUCTURE: 3})
ROCKET_SCIENCE = Item("Rocket science", 80, 8,
                      {EMPTY_BARREL: 1, SOLID_ROCKET_FUEL: 1, SPACE_PLATFORM: 1, SOLAR_PANEL: 1, VULCANITE_BLOCK: 1,
                       MACHINE_LEARNING_DATA: 1, CHEMICAL_GEL: 2}, factory_speed=S_MANUFACTORY)
ALL_SCIENCE = Item("All science packs", 1, 1, {AUTOMATION_SCIENCE: 1, LOGISTIC_SCIENCE: 1, MILITARY_SCIENCE: 1, 
                                               CHEMICAL_SCIENCE: 1})

# Modules
SPEED_MODULE_1 = Item("Speed module", 2, 1, {ELECTRONIC_CIRCUIT: 5, ADVANCED_CIRCUIT: 1})
SPEED_MODULE_2 = Item("Speed module 2", 4, 1, {ADVANCED_CIRCUIT: 5, PROCESSING_UNIT: 1, SPEED_MODULE_1: 3})
SPEED_MODULE_3 = Item("Speed module 2", 8, 1, {PROCESSING_UNIT: 5, BATTERY: 1, SPEED_MODULE_2: 3})

# MOTOR.analyze(5)
# ELECTRONIC_CIRCUIT.analyze(4)
# FAST_INSERTER.analyze(0.5)

# ELECTRONIC_CIRCUIT.analyze(10)
# ADVANCED_CIRCUIT.analyze(12, ignore=[ELECTRONIC_CIRCUIT])
# GLASS.analyze(6)
# PROCESSING_UNIT.analyze(10, ignore=[ELECTRONIC_CIRCUIT, ADVANCED_CIRCUIT])

# AUTOMATION_SCIENCE.analyze(num_per_second_needed=1.25)
# LOGISTIC_SCIENCE.analyze(num_per_second_needed=1.25)
# MILITARY_SCIENCE.analyze(num_per_second_needed=1.25)
# CHEMICAL_SCIENCE.analyze(num_per_second_needed=1.25)
PRODUCTION_SCIENCE.analyze(num_per_second_needed=1.25, ignore=[ELECTRONIC_CIRCUIT, ADVANCED_CIRCUIT])
# UTILITY_SCIENCE.analyze(num_per_second_needed=1.25, ignore=[PROCESSING_UNIT, PLASTIC_BAR, BATTERY, ELECTRONIC_CIRCUIT])
# ROCKET_SCIENCE.analyze(4, ignore=[GLASS, ELECTRONIC_CIRCUIT, ADVANCED_CIRCUIT, PROCESSING_UNIT, SOLAR_PANEL, 
#                                   SPACE_PLATFORM, EMPTY_BARREL, VULCANITE_BLOCK, LUBRICANT, SOLID_ROCKET_FUEL, SULFUR,
#                                   ROUGH_DS_SUBSTRATE])
# ALL_SCIENCE.analyze(1)

# ENGINE_UNIT.analyze(10)

# TRANSPORT_BELT.analyze(1)

# FIREARM_MAGAZINE.analyze(num_per_second_needed=3)
# PIERCING_MAGAZINE.analyze(num_per_second_needed=3)
# ARTILLERY_SHELL.analyze(1, ignore=[ELECTRONIC_CIRCUIT, PLASTIC_BAR])

# FLYING_ROBOT_FRAME.analyze(4, ignore=[BATTERY, ELECTRONIC_CIRCUIT, ELECTRIC_ENGINE])
# SOLAR_PANEL.analyze(8)
# ACCUMULATOR.analyze(20)
# LASER_TURRET.analyze(4, ignore=[SULFURIC_ACID, GLASS, BATTERY, ELECTRONIC_CIRCUIT])

# SULFURIC_ACID.analyze(3)

# FLYING_ROBOT_FRAME.analyze(1, ignore=[SULFURIC_ACID, ELECTRIC_MOTOR, ELECTRONIC_CIRCUIT, ENGINE_UNIT])

# LOW_DENSITY_STRUCTURE.analyze(num_per_second_needed=1/3, ignore=[PLASTIC_BAR, GLASS])
# ROCKET_CONTROL_UNIT.analyze(num_per_second_needed=1/3, ignore=[PROCESSING_UNIT, ADVANCED_CIRCUIT, BATTERY, GLASS])
# HEAT_SHIELDING.analyze(num_per_second_needed=1/3)
# SOLID_ROCKET_FUEL.analyze(num_per_second_needed=2/3)

# ROCKET_PART.analyze(1, ignore=[LOW_DENSITY_STRUCTURE, ROCKET_CONTROL_UNIT, HEAT_SHIELDING, SOLID_ROCKET_FUEL])

# SPEED_MODULE_3.analyze(1, ignore=[ELECTRONIC_CIRCUIT, ADVANCED_CIRCUIT, PROCESSING_UNIT, BATTERY])

# LOGISTIC_SCIENCE.count(100)
# ROCKET_SCIENCE.count(800, ignore=[GLASS, ELECTRONIC_CIRCUIT, ADVANCED_CIRCUIT, PROCESSING_UNIT, SOLAR_PANEL, 
#                                   SPACE_PLATFORM, EMPTY_BARREL, VULCANITE_BLOCK, LUBRICANT, SOLID_ROCKET_FUEL, SULFUR, 
#                                   ROUGH_DS_SUBSTRATE])
