import random

races = {"Dwarf":"CON",
         "Elf":"INT",
         "Gnome":"CHA",
         "Half Elf":"WIS",
         "Half Orc":"STR",
         "Halfling":"DEX",
         "Human":"ANY"}
##classes = {"Barbarian":"STR",
##           "Bard":"CHA",
##           "Cleric":"WIS",
##           "Druid":"WIS",
##           "Fighter":"CON",
##           "Monk":"STR",
##           "Paladin":"CON",
##           "Ranger":"DEX",
##           "Rogue":"DEX",
##           "Sorceror":"CHA",
##           "Wizard":"INT"}
classes = {"Barbarian": ["STR","CON"],
           "Bard":      ["CHA","INT"],
           "Cleric":    ["WIS","CHA"],
           "Druid":     ["WIS"],
           "Fighter":   ["STR","DEX"],
           "Monk":      ["WIS","DEX"],
           "Paladin":   ["CON","CHA"],
           "Ranger":    ["DEX","WIS"],
           "Rogue":     ["DEX","INT"],
           "Sorceror":  ["CHA"],
           "Wizard":    ["INT"]}
apg_classes = {"Alchemist": ["INT","DEX"],
               "Cavalier":  ["STR","DEX"],
               "Gunslinger":["DEX","WIS"],
               "Inquisitor":["WIS","STR"],
               "Magus":     ["STR","INT"],
               "Oracle":    ["CHA"],
               "Summoner":  ["CHA","DEX"],
               "Witch":     ["INT"]}
classes = dict(classes.items() + apg_classes.items())
attr_list = ["STR","DEX","CON","INT","WIS","CHA"]

def d(n,d,DropLowest=False):
    if DropLowest:
        return sum(sorted([random.randint(1,d) for x in xrange(n)])[1:])
    else:
        return sum([random.randint(1,d) for x in xrange(n)])

r = random.choice(races.keys())
c = random.choice(classes.keys())
##key_attr = [races[r], classes[c]]
##if key_attr[0] == "ANY":
##    key_attr[0] = random.choice(attr_list)
##
##attr = []
##for a in attr_list:
##    if a in key_attr:
##        if key_attr.count(a) > 1:
##            attr.append(18)
##        else:
##            attr.append(16)
##    else:
##        attr.append(d(4,6,DropLowest=True))
key_attr = classes[c]

attr = []
for a in attr_list:
    if a in key_attr:
        if len(key_attr) > 1:
            if key_attr[0] == a:
                attr.append(16)
            else:
                attr.append(15)
        else:
            attr.append(18)
    else:
        attr.append(d(4,4,DropLowest=False))

print r, c
print attr
