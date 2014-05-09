# -*- coding: cp1252 -*-
import random, time, gc
##from scipy import weave
##from scipy.weave import converters

def d(n,d):
    return sum([random.randint(1,d) for i in xrange(n)])

def dice(n,d,explode=[],min_roll=1):
    i = 0
    t = 0
    while i < n:
        r = max(random.randint(1,d),min_roll)
        t += r
        if not (r in explode):
            i += 1
    return t

def weapon_attack(n,dice,crit=20,mult=2,ac=10,bonus=0):
##    atk = weave.inline(dice_code,
##                       ['n', 'dice'],
##                       type_converters=converters.blitz,
##                       compiler = 'gcc')
    atk = d(1,20)
    crit_conf = d(1,20)
    dmg = 0
    gotcrit = False
    if atk >= ac or atk == 20:
        dmg = d(n,dice) + bonus
        if atk >= crit and (crit_conf >= ac or crit_conf == 20):
            dmg += d(n*(mult-1),dice) + bonus*(mult-1)
            gotcrit = True
    return dmg, gotcrit

##dice_code = """
##            int a = 0
##            for(int i=0;i < n;i++){
##                a = a + random(100 - 1)
##            }
##            return a
##            """

def print_graph(dmg_list, brief=True, scale=1):
    for i in xrange(min(dmg_list),max(dmg_list)+1):
        c = dmg_list.count(i) // scale
        if not brief:
            display = "I"*c
        elif dmg_list.count(i):
            display = c
        else:
            display = ""
        print "{0}:\t{1}".format(i,display)

def print_stats(l):
    if not l: l = [0]
    mn = mean(l)
    print "Mean:", mn
    print "Median:", median(l)
    print "Mode:", mode(l)
    print "Standard Deviation:", stddev(l, mn)

def mean(l):
    return float(sum(l))/len(l)

def median(numericValues):
  theValues = sorted(numericValues)

  if len(theValues) % 2 == 1:
    return theValues[(len(theValues)+1)/2-1]
  else:
    lower = theValues[len(theValues)/2-1]
    upper = theValues[len(theValues)/2]

    return (float(lower + upper)) / 2

def mode(alist):
    mode = None
    mode_count = 0
    no_dups = list(set(alist))
    for i in no_dups:
##        print i,alist.count(i)," ",
        if alist.count(i) > mode_count:
            mode = i
            mode_count = alist.count(i)
##    print ""
    return mode, mode_count, "{0:.1%}".format(float(mode_count)/len(alist))

def stddev(l, m=None):
    if not m:
        m = mean(l)
    stddev_l = [(m-n)**2 for n in l]
    return mean(stddev_l)**0.5

def RunWeaponSim(n,dice,crit,mult):
    ac = 10
    keen = False
    oncrit = (0,0,0) # {1}d{2}+{3} whenever you crit
    
    rounds = 300000
    brief = False
    bonus = 0
    scale = 1

    if keen:
        crit = 2*crit-21 # Double threat range
    l = []
    crits = 0
    for i in xrange(rounds):
        r = weapon_attack(n,dice,crit,mult,ac,bonus)
        l.append(r[0])
##        if r[1]:
##            crits += 1
##            l[-1] += d(oncrit[0],oncrit[1]) + oncrit[2]
##    print "Hits:\t", len(l)-l.count(0)
##    print "Crits:\t", crits
##    print_graph(l, brief, scale)
##    print_stats(l)
##    print "Total damage:",sum(l)
    print_stats([x for x in l if x != 0])

gc.disable() # Disable garbage collection
t = time.clock()

##print ""
##print "Chakram 1d8 x2"
##RunWeaponSim(1,8,20,2)
##
##print ""
##print "Shortbow 1d6 x3"
##RunWeaponSim(1,6,20,3)
##
##print ""
##print "Longsword 1d8 19-20/x2"
##RunWeaponSim(1,8,19,2)
##
##print ""
##print "Broadsword 2d4 x2"
##RunWeaponSim(2,4,20,2)

print ""
print "Scimitar 1d6 18-20/x2"
RunWeaponSim(1,6,18,2)

##
##print ""
##print "Greataxe 1d12 x3"
##RunWeaponSim(1,12,20,3)

print ""
print "Greatsword 2d6 19–20/x2"
RunWeaponSim(2,6,19,2)

##print ""
##print "Greataxe (small) 1d10 x3"
##RunWeaponSim(1,10,20,3)
##
##print ""
##print "Greatsword (small) 1d10 19–20/x2"
##RunWeaponSim(1,10,19,2)
##
##print ""
##print "Greataxe (large) 3d6 x3"
##RunWeaponSim(3,6,20,3)
##
##print ""
##print "Greatsword 3d6 19–20/x2"
##RunWeaponSim(3,6,19,2)
##
##print ""
##print "Earth breaker 2d6 x3"
##RunWeaponSim(2,6,20,3)
##
##print ""
##print "Falchion 2d4 18-20/x2"
##RunWeaponSim(2,4,18,2)
##
##print ""
##print "Pickaxe 1d8 x4"
##RunWeaponSim(1,8,20,4)
##
##print ""
##print "Bardiche 1d10 19-20/x2"
##RunWeaponSim(1,10,19,2)
##
##print ""
##print "Bec de Corbin 1d10 x3"
##RunWeaponSim(1,10,20,3)
##
##print ""
##print "Guisarme 2d4 x3"
##RunWeaponSim(2,4,20,3)
##
##print ""
##print "Guisarme 1d10 x3"
##RunWeaponSim(1,10,20,3)
##
##a = [d(3,8)+7 for i in xrange(50000)]
##b = [d(7,6) for i in xrange(50000)]
##c = [dice(4,6,min_roll=2) for i in xrange(100000)]

##a = [1,2,3,4,5,6]
##b = [1,3,4,6]
##print_stats(a)
##print_stats(b)

##print mean([d(20,6) for i in xrange(100000)]), time.clock()-t
##print mean([dice(20,6) for i in xrange(100000)]), time.clock()-t

print ""
print time.clock()-t
