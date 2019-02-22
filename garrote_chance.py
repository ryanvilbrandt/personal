# Measures likelihood that an NPC that gets hit with a garrote will have at least one turn to act
# Checks for number of rounds of suffocation and the chance of a surprise round
# Garrote: http://private-5e.wikidot.com/equipment:weapons

from glob import glob
import re
from os.path import join

bestiary_folder = r"C:\Users\ryan.v\Documents\GitHub\bestiary\_posts"

bestiary = []

for filename in glob(join(bestiary_folder, "*.markdown")):
    with open(filename) as f:
        try:
            text = f.read()
        except Exception as e:
            print(filename)
            print(e)
            continue
        m = re.search(r"tags: \[(.*?)\]", text)
        if not m:
            continue
        if "humanoid" in m.group(1):
            m = re.search(r"\| (.*?) \((.*?)\) \| (.*?) \((.*?)\) \| (.*?) \((.*?)\) \| "
                          r"(.*?) \((.*?)\) \| (.*?) \((.*?)\) \| (.*?) \((.*?)\) \|", text)
            if not m:
                continue
            str_mod = int(m.group(2))
            dex_mod = int(m.group(4))
            con_mod = int(m.group(6))

            skills = ""
            m = re.search(r"\*\*Skills\*\* (.*?)\n", text)
            if m:
                skills = m.group(1)

            m = re.search(r'title: "(.*?)"', text)
            if not m:
                continue
            name = m.group(1)
            bestiary.append([name, str_mod, dex_mod, con_mod, skills])

print(bestiary)


names, str_mods, dex_mods, con_mods, skills = zip(*bestiary)
average_dex_mod = sum(dex_mods) / len(dex_mods)
print(average_dex_mod)

con_mods_higher_than_one = 0
for c in con_mods:
    if c > 1:
        con_mods_higher_than_one += 1
chance_of_high_con_mod = con_mods_higher_than_one / len(con_mods)
print(chance_of_high_con_mod)

chance_of_not_surprise = 0.5 - ((5 - average_dex_mod) * 0.05)
print(chance_of_not_surprise)

print(1 - ((1 - chance_of_not_surprise) * (1 - chance_of_high_con_mod)))

# humanoids_with_athletics_acrobatics = 0
# for b in bestiary:
#     if "Athletics" in b[4]:
#         print(b[0])
#         print(b[4])
#         m = re.search("Athletics \+(\d+)", b[4])
#         print(m.group(1))
#         humanoids_with_athletics_acrobatics += 1
# print(humanoids_with_athletics_acrobatics/len(skills))


escape_bonuses = []
for b in bestiary:
    m = re.search("Athletics \+(\d+)", b[4])
    athletics_bonus = int(m.group(1)) if m else 0
    m = re.search("Acrobatics \+(\d+)", b[4])
    acrobatics_bonus = int(m.group(1)) if m else 0
    bonus = max(athletics_bonus, acrobatics_bonus)
    if bonus > 0:
        escape_bonuses.append(bonus)
print(sum(escape_bonuses) / len(escape_bonuses))