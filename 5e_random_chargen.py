import random
import unittest

class TestRollStats(unittest.TestCase):

    def setUp(self):
        # Replace randint with a deterministic function
        def randint_test(a, b):
            # randint_test(1, 6) == 3
            return int((b+a)/2)
        random.randint = randint_test

    def test_randint(self):
        self.assertEqual(random.randint(1, 6), 3)

    def test_rollstats_default(self):
        result = ", ".join(["9"]*6)
        self.assertEqual(RollStats(), result)

    def test_rollstats_four_dice(self):
        result = ", ".join(["12"]*6)
        self.assertEqual(RollStats(n=5), result)

    def test_rollstats_8_stats(self):
        result = ", ".join(["9"]*8)
        self.assertEqual(RollStats(iters=8), result)

    def test_rollstats_4d6_drop_lowest(self):
        result = ", ".join(["9"]*6)
        self.assertEqual(RollStats(n=4, drop_lowest=True), result)

races = [
    ['Hill Dwarf', 'Mountain Dwarf'],
    ['High Elf', 'Wood Elf', 'Dark Elf'],
    ['Lightfoot Halfling', 'Stout Halfling'],
    ['Human'],
    [
        'Dragonborn',
        ['Forest Gnome', 'Rock Gnome'],
        'Half-Elf',
        'Half-Orc',
        'Tiefling'
    ]
]

classes = [
    ['Berserker Barbarian', 'Totem Warrior Barbarian'],
    ['Bard of Lore', 'Bard of Valor'],
    ['Cleric of Knowledge', 'Cleric of Life', 'Cleric of Light',
     'Cleric of Nature', 'Cleric of the Tempest', 'Cleric of Trickery'],
    ['Druid of the Land', 'Druid of the Moon'],
    ['Champion Fighter', 'Battle Master Fighter', 'Eldritch Knight Fighter'],
    ['Monk of the Open Hand', 'Monk of Shadow', 'Monk of the Four Elements'],
    ['Paladin of Devotion', 'Paladin of the Ancients', 'Paladin of Vengeance'],
    ['Hunter Ranger', 'Beast Master Ranger'],
    ['Thief Rogue', 'Assassin Rogue', 'Arcane Trickster Rogue'],
    ['Draconic Sorcerer', 'Wild Magic Sorcerer'],
    ['Warlock of the Archfey', 'Warlock of the Fiend',
     'Warlock of the Great Old One'],
    ['Abjuration Wizard', 'Conjuration Wizard', 'Divination Wizard',
     'Enchantment Wizard', 'Evocation Wizard', 'Illusion Wizard',
     'Necromancy Wizard', 'Transmutation Wizard']
]

backgrounds = ['Acolyte', 'Charlatan', 'Criminal', 'Entertainer', 'Folk Hero',
               'Guild Artisan', 'Hermit', 'Noble', 'Outlander', 'Sage',
               'Sailor', 'Soldier', 'Urchin']

def PickRandomItem(array):
    pick = random.choice(array)
    if isinstance(pick, list):
        return PickRandomItem(pick)
    else:
        return pick

def RollStats(n=4, d=6, iters=6, drop_lowest=True, bonus=0):
    # Build a list of stats
    stats = []
    for _ in xrange(iters):
        # Roll n dice, each with d-sides
        dice_results = [random.randint(1, d) for i in xrange(n)]
        # Sum the results
        total = sum(dice_results)+bonus
        if drop_lowest:
            # Drop the lowest roll
            total -= min(dice_results)
        # Add the total to the list of results
        stats.append(str(total))
    return ", ".join(stats)

def DistributeStats(n=12, starting_value=9):
    '''
    All ability scores start at 9. Roll n dice.
    Add +1 to the score depending on the die roll.
    '''
    array_size = 6
    starting_array = [starting_value]*array_size
    for i in xrange(n):
        starting_array[random.randint(0, array_size-1)] += 1
    return ", ".join([str(s) for s in starting_array])

def main():
    print RollStats()
    ##print DistributeStats()
    print "{}, {}, {}".format(
        PickRandomItem(races),
        PickRandomItem(classes),
        PickRandomItem(backgrounds)
        )
    print "Specialty: {}, Personality: {}".format(
        random.randint(1, 8),
        random.randint(1, 8)
        )
    print "Ideal: {}, Bond: {}, Flaw: {}".format(
        random.randint(1, 6),
        random.randint(1, 6),
        random.randint(1, 6)
        )

main()
# try:
#    unittest.main()
# except SystemExit:
#    pass
