#!/usr/bin/env python
# -*- coding: cp1252 -*-
import random, re

WONDER_TABLE = {1: "Target affected by slow for 10 rounds (Will DC 15 negates).\nhttp://www.d20pfsrd.com/magic/all-spells/s/slow",
                6: "Faerie fire surrounds the target for 10 minutes.\nhttp://www.d20pfsrd.com/magic/all-spells/f/faerie-fire",
                10: "Deludes the wielder for 1 round into believing the rod functions as indicated by a second die roll (no save).",
                16: "Gust of wind, but at windstorm force (Fortitude DC 14 negates).\nhttp://www.d20pfsrd.com/magic/all-spells/g/gust-of-wind",
                21: "Wielder learns the target's surface thoughts (as with detect thoughts) for 1d4 rounds (no save).\nhttp://www.d20pfsrd.com/magic/all-spells/d/detect-thoughts",
                26: "Stinking cloud appears at 30-foot range for 10 rounds (Fortitude DC 15 negates).\nhttp://www.d20pfsrd.com/magic/all-spells/s/stinking-cloud",
                31: "Heavy rain falls for 1 round in 60-foot radius centered on the rod wielder.",
                34: "Summons an animal—a rhino (01—25 on d%), elephant (26—50), or mouse (51—100).",
                37: "Lightning bolt (70 foot long, 5 foot wide), 6d6 points of damage (Reflex DC 15 half).\nhttp://www.d20pfsrd.com/magic/all-spells/l/lightning-bolt",
                47: "A stream of 600 large butterflies pours forth and flutters around for 2 rounds, blinding everyone within 25 feet (Reflex DC 14 negates).\nhttp://www.d20pfsrd.com/gamemastering/conditions#TOC-Blinded",
                50: "Target is affected by enlarge person if within 60 feet of rod for 10 minutes (Fortitude DC 13 negates).\nhttp://www.d20pfsrd.com/magic/all-spells/e/enlarge-person",
                54: "Darkness, 30-foot-diameter hemisphere, centered 30 feet away from rod, for 10 minutes.\nhttp://www.d20pfsrd.com/magic/all-spells/d/darkness",
                59: "Grass grows in 160-square-foot area before the rod, or grass existing there grows to 10 times its normal size.",
                63: "Any nonliving object of up to 1,000 pounds of mass and up to 30 cubic feet in size turns ethereal.\nhttp://www.d20pfsrd.com/gamemastering/special-abilities#TOC-Ethereal",
                66: "Reduce wielder two size categories (no save) for 1 day.",
                70: "Fireball at target or 100 feet straight ahead, 6d6 points of damage (Reflex DC 15 half).\nhttp://www.d20pfsrd.com/magic/all-spells/f/fireball",
                80: "Invisibility covers the rod's wielder for 10 minutes.\nhttp://www.d20pfsrd.com/magic/all-spells/i/invisibility",
                85: "Leaves grow from the target if within 60 feet of the rod. These last 24 hours.",
                88: "10—40 gems, value 1 gp each, shoot forth in a 30-foot-long stream. Each gem deals 1 point of damage to any creature in its path: roll 5d4 for the number of hits and divide them among the available targets.",
                91: "Shimmering colors dance and play over a 40-foot-by-30-foot area in front of rod. Creatures therein are blinded for 1d6 rounds (Fortitude DC 15 negates).\nhttp://www.d20pfsrd.com/gamemastering/conditions#TOC-Blinded",
                96: "Wielder (50% chance) or the target (50% chance) turns permanently blue, green, or purple (no save).",
                98: "Flesh to stone (or stone to flesh if the target is stone already) if the target is within 60 feet (Fortitude DC 18 negates).\nhttp://www.d20pfsrd.com/magic/all-spells/f/flesh-to-stone\nhttp://www.d20pfsrd.com/magic/all-spells/s/stone-to-flesh"
                }

def GetFromTable(table):
    '''Requires a dictionary where all keys are ints > 0'''
    keys = table.keys()
    r = random.randint(1,max(keys))
    return min(filter(lambda x: x >= r, keys))

def ParseDice(s):
    if s == "":
        return s
    regex = r"(\d+d\d+)" # Matches "1d8", "12d6", "1d20", etc
    m = re.findall(regex, s)
    for x in set(m):
        s = s.replace(x,str(RollDice(x)))
    return s

def RollDice(s):
    n,p,d = s.partition('d')
    try:
        n = int(n)
        d = int(d)
    except ValueError:
        return 0
    return sum([random.randint(1,d) for i in xrange(n)])

temp = WONDER_TABLE[GetFromTable(WONDER_TABLE)]

if temp == "Summons an animal—a rhino (01—25 on d%), elephant (26—50), or mouse (51—100).":
    r = random.randint(1,4)
    if r == 1:
        s1 = "rhino."
        s2 = "\nhttp://www.d20pfsrd.com/bestiary/monster-listings/animals/rhinoceros"
    elif r == 2:
        s1 = "elephant."
        s2 = "\nhttp://www.d20pfsrd.com/bestiary/monster-listings/animals/elephant"
    else:
        s1 = "mouse."
        s2 = ""
    print "Summons a {0} for 10 rounds.{1}".format(s1,s2)
elif temp == "10—40 gems, value 1 gp each, shoot forth in a 30-foot-long stream. Each gem deals 1 point of damage to any creature in its path: roll 5d4 for the number of hits and divide them among the available targets.":
    print "{0} gems, value 1 gp each, shoot forth in a 30-foot-long stream. Each gem deals 1 point of damage to any creature in its path; divide the hits among the available targets.".format(RollDice("10d4"))
elif temp == "Wielder (50% chance) or the target (50% chance) turns permanently blue, green, or purple (no save).":
    s1 = "Wielder" if random.randint(1,2) == 1 else "Target"
    r = random.randint(1,3)
    if r == 1:
        s2 = "blue"
    elif r == 2:
        s2 = "green"
    else:
        s2 = "purple"
    print "{0} turns permanently {1} (no save).".format(s1, s2)
else:
    temp = ParseDice(temp)
    print temp
