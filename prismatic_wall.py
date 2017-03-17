import random

def dice(n, d, mod=0, roll_type=None, dc=None):
    result = sum([random.randint(1, d) for _ in xrange(n)])
    if roll_type is not None:
        result_2 = sum([random.randint(1, d) for _ in xrange(n)])
        if roll_type == "advantage":
            result = max(result, result_2)
        elif roll_type == "disadvantage":
            result = min(result, result_2)
    if dc is None:
        return result + mod
    return result + mod >= dc

def prismatic_wall(name, dex_save, con_save, wis_save, spell_dc=18):
    print "{} tries to pass through the Prismatic Wall!".format(name)
    total_damage = 0

    if not dice(1, 20, con_save, dc=spell_dc):
        print "{} is blinded by the dazzling colors!".format(name)

    # Red layer, 10d6 fire damage
    damage = dice(10, 6)
    saved = dice(1, 20, dex_save, dc=spell_dc)
    if saved:
        damage /= 2
    print "{} takes {} fire damage ({})".format(name, damage, "saved" if saved else "failed")
    total_damage += damage

    # Orange layer, 10d6 acid damage
    damage = dice(10, 6)
    saved = dice(1, 20, dex_save, dc=spell_dc)
    if saved:
        damage /= 2
    print "{} takes {} acid damage ({})".format(name, damage, "saved" if saved else "failed")
    total_damage += damage

    # Yellow layer, 10d6 lightning damage
    damage = dice(10, 6)
    saved = dice(1, 20, dex_save, dc=spell_dc)
    if saved:
        damage /= 2
    print "{} takes {} lightning damage ({})".format(name, damage, "saved" if saved else "failed")
    total_damage += damage

    # Green layer, 10d6 poison damage
    damage = dice(10, 6)
    saved = dice(1, 20, dex_save, dc=spell_dc)
    if saved:
        damage /= 2
    print "{} takes {} poison damage ({})".format(name, damage, "saved" if saved else "failed")
    total_damage += damage

    # Blue layer, 10d6 cold damage
    damage = dice(10, 6)
    saved = dice(1, 20, dex_save, dc=spell_dc)
    if saved:
        damage /= 2
    print "{} takes {} cold damage ({})".format(name, damage, "saved" if saved else "failed")
    total_damage += damage
    print "{} took a total of {} damage. Poor sap.".format(name, total_damage)

    # Indigo layer, save against petrification
    saved = dice(1, 20, dex_save, dc=spell_dc)
    if not saved:
        print "{} is restrained by the Indigo layer!".format(name)
        passes, fails = 0, 0
        while True:
            if dice(1, 20, con_save, dc=spell_dc):
                print "{} passed their Con save!".format(name)
                passes += 1
            else:
                print "{} failed their Con save!".format(name)
                fails += 1
            if fails >= 3:
                print "{} was turned to stone!".format(name)
                return
            if passes >= 3:
                print "{} has fought off the effects of the Indigo layer! The prismatic wall disappears!".format(name)
                return
    else:
        print "{} passes through the Indigo layer safely!".format(name)

    # Violet layer, save against blindness
    saved = dice(1, 20, dex_save, dc=spell_dc)
    if not saved:
        print "{} is blinded by the Violet layer!".format(name)
        if dice(1, 20, wis_save, dc=spell_dc):
            print "{} is no longer blinded.".format(name)
        else:
            print "{} disappears from this plane in a flash of violet light!".format(name)
            return
    else:
        print "{} passes through the Violet layer safely!".format(name)
    print "{} made it through the Prismatic Wall!"


prismatic_wall("Orc 3", 3, 5, -1)
