from collections import defaultdict
from math import ceil

ROUND_FACTORIES = False


class Item:

    def __init__(self, name, crafting_time=1.0, num_created=1, recipe=None):
        self.name = name
        self.crafting_time = crafting_time
        self.num_created = num_created
        self.recipe = recipe
        self.is_raw_material = recipe is None
        self.num_per_second = 0.0 if self.is_raw_material else (num_created / crafting_time)

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
        print("{}{}".format("  " * indent, self.name))
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
IRON_ORE = Item("Iron ore")
COPPER_ORE = Item("Copper ore")
COAL = Item("Coal")
WATER = Item("Water")
STONE = Item("Stone")
CRUDE_OIL = Item("Crude Oil")
SILICON_ORE = Item("Silicon ore")
TITANIUM_ORE = Item("Titanium ore")

# Smelted goods
IRON_INGOT = Item("Iron ingot", 1, 1, {IRON_ORE: 1})
COPPER_INGOT = Item("Copper ingot", 1, 1, {COPPER_ORE: 1})
STONE_BRICK = Item("Stone brick", 1, 1, {STONE: 1})
STEEL = Item("Steel", 3, 1, {IRON_INGOT: 3})
HIGH_PURITY_SILICON = Item("High-purity silicon", 1, 2, {SILICON_ORE: 2})
TITANIUM_INGOT = Item("Titanium ingot", 1, 2, {TITANIUM_ORE: 2})
GLASS = Item("Glass", 2, 1, {STONE: 2})
TITANIUM_GLASS = Item("Titanium glass", 5, 2, {GLASS: 2, TITANIUM_INGOT: 2, WATER: 2})
ENERGETIC_GRAPHITE = Item("Energetic Graphite", 2, 1, {COAL: 2})
DIAMOND = Item("Diamond", 2, 1, {ENERGETIC_GRAPHITE: 1})

# Oil goods
REFINED_OIL = Item("Refined Oil", 4, 2, {CRUDE_OIL: 2})
HYDROGEN = Item("Hydrogen", 4, 1, {CRUDE_OIL: 2})
# HYDROGEN = Item("Hydrogen (x-ray)", 4, 3, {CRUDE_OIL: 2})
# HYDROGEN = Item("Hydrogen (gas giant)")
SULFURIC_ACID = Item("Sulfuric Acid", 6, 4, {REFINED_OIL: 6, STONE: 8, WATER: 4})
DEUTERIUM = Item("Deuterium", 5, 5, {HYDROGEN: 10})

# Processed goods
PLASTIC = Item("Plastic", 3, 1, {REFINED_OIL: 2, ENERGETIC_GRAPHITE: 1})
CRYSTAL_SILICON = Item("Crystal silicon", 2, 1, {HIGH_PURITY_SILICON: 1})
GRAPHENE = Item("Graphene", 3, 2, {ENERGETIC_GRAPHITE: 3, SULFURIC_ACID: 1})
CARBON_NANOTUBE = Item("Carbon nanotube", 4, 2, {GRAPHENE: 3, TITANIUM_INGOT: 1})
PARTICLE_BROADBAND = Item("Particle broadband", 8, 1, {CARBON_NANOTUBE: 2, CRYSTAL_SILICON: 2, PLASTIC: 1})
PRISM = Item("Prism", 2, 2, {GLASS: 3})
ORGANIC_CRYSTAL = Item("Organic crystal", 6, 1, {PLASTIC: 2, REFINED_OIL: 1, WATER: 1})
TITANIUM_CRYSTAL = Item("Titanium crystal", 4, 1, {ORGANIC_CRYSTAL: 1, TITANIUM_INGOT: 3})
TITANIUM_ALLOY = Item("Titanium alloy", 12, 4, {TITANIUM_INGOT: 4, STEEL: 4, SULFURIC_ACID: 8})

# Machine parts
GEAR = Item("Gear", 1, 1, {IRON_INGOT: 1})
MAGNET = Item("Magnet", 1.5, 1, {IRON_ORE: 1})
MAGNETIC_COIL = Item("Magnetic coil", 1, 2, {MAGNET: 2, COPPER_INGOT: 1})
ELECTRIC_MOTOR = Item("Electric motor", 2, 1, {IRON_INGOT: 2, GEAR: 1, MAGNETIC_COIL: 1})
ELECTROMAGNETIC_TURBINE = Item("Electromagnetic turbine", 2, 1, {ELECTRIC_MOTOR: 2, MAGNETIC_COIL: 2})
SUPER_MAGNETIC_RING = Item("Super-magnetic ring", 3, 1, {ELECTROMAGNETIC_TURBINE: 2, MAGNET: 3, ENERGETIC_GRAPHITE: 1})

# Made-up quantum shit
PARTICLE_CONTAINER = Item("Particle container", 4, 1, {ELECTROMAGNETIC_TURBINE: 2, COPPER_INGOT: 2, GRAPHENE: 2})
CASIMIR_CRYSTAL = Item("Casimir crystal", 4, 1, {TITANIUM_CRYSTAL: 1, GRAPHENE: 2, HYDROGEN: 12})
STRANGE_MATTER = Item("Strange matter", 8, 1, {PARTICLE_CONTAINER: 2, IRON_INGOT: 2, DEUTERIUM: 10})
GRAVITON_LENS = Item("Graviton lens", 6, 1, {DIAMOND: 4, STRANGE_MATTER: 1})
PLANE_FILTER = Item("Plane filter", 12, 1, {CASIMIR_CRYSTAL: 1, TITANIUM_GLASS: 2})

# Electronics
CIRCUIT_BOARD = Item("Circuit board", 1, 2, {IRON_INGOT: 2, COPPER_INGOT: 1})
MICROCRYSTALLINE_COMPONENT = Item("Microcrystalline component", 2, 1, {HIGH_PURITY_SILICON: 2, COPPER_INGOT: 1})
PROCESSOR = Item("Processor", 3, 1, {CIRCUIT_BOARD: 2, MICROCRYSTALLINE_COMPONENT: 2})
QUANTUM_PROCESSOR = Item("Quantum processor", 6, 1, {PROCESSOR: 2, PLANE_FILTER: 2})
DEUTERIUM_FUEL_ROD = Item("Deuterium fuel rod", 6, 1, {TITANIUM_ALLOY: 1, DEUTERIUM: 10, SUPER_MAGNETIC_RING: 1})

# Dyson sphere stuff
PHOTON_COMBINER = Item("Photon combiner", 3, 1, {PRISM: 2, CIRCUIT_BOARD: 1})
SOLAR_SAIL = Item("Solar sail", 4, 2, {GRAPHENE: 1, PHOTON_COMBINER: 1})
FRAME_MATERIAL = Item("Frame material", 6, 1, {CARBON_NANOTUBE: 4, TITANIUM_ALLOY: 1, HIGH_PURITY_SILICON: 1})
DYSON_SPHERE_COMPONENT = Item("Dyson sphere component", 8, 1, {FRAME_MATERIAL: 3, SOLAR_SAIL: 3, PROCESSOR: 3})
SMALL_CARRIER_ROCKET = Item("Small carrier rocket", 6, 1, {DYSON_SPHERE_COMPONENT: 2, DEUTERIUM_FUEL_ROD: 2, QUANTUM_PROCESSOR: 2})


# Factory equipment


# SCIENCE!
ELECTROMAGNETIC_MATRIX = Item("Electromagnetic matrix", 3, 1, {MAGNETIC_COIL: 1, CIRCUIT_BOARD: 1}) 
ENERGY_MATRIX = Item("Energy matrix", 6, 1, {ENERGETIC_GRAPHITE: 2, HYDROGEN: 2})
STRUCTURE_MATRIX = Item("Structure matrix", 8, 1, {DIAMOND: 1, TITANIUM_CRYSTAL: 1})
INFORMATION_MATRIX = Item("Information matrix", 10, 1, {PROCESSOR: 2, PARTICLE_BROADBAND: 1})
GRAVITY_MATRIX = Item("Gravity matrix", 24, 2, {GRAVITON_LENS: 1, QUANTUM_PROCESSOR: 1})
ALL_MATRICES = Item("All matrices", 1, 1, {ELECTROMAGNETIC_MATRIX: 1, ENERGY_MATRIX: 1, STRUCTURE_MATRIX: 1, INFORMATION_MATRIX: 1, GRAVITY_MATRIX: 1})

# INFORMATION_MATRIX.analyze(num_per_second_needed=1)
# GRAVITY_MATRIX.analyze(num_per_second_needed=1)
# ALL_MATRICES.analyze(num_per_second_needed=1, ignore=[CIRCUIT_BOARD, MAGNETIC_COIL, ENERGETIC_GRAPHITE, HYDROGEN, DIAMOND, TITANIUM_CRYSTAL, PROCESSOR, PARTICLE_BROADBAND, GRAVITON_LENS, QUANTUM_PROCESSOR])
# SOLAR_SAIL.analyze(num_per_second_needed=1, ignore=[GRAPHENE])
# ELECTRIC_MOTOR.analyze(8, ignore=[MAGNETIC_COIL, IRON_INGOT])
# SULFURIC_ACID.analyze(18, ignore=[REFINED_OIL])
# SMALL_CARRIER_ROCKET.analyze(num_per_second_needed=1, ignore=[DEUTERIUM_FUEL_ROD, QUANTUM_PROCESSOR, PROCESSOR, FRAME_MATERIAL, GRAPHENE, PHOTON_COMBINER])
PROCESSOR.analyze(9)
