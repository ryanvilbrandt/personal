import random

prob_list = [0,0,0,-14,-11,-8,-6,-4,-2,-1,0,1,2,3,5,7,10,13,17]

def d(n,d,num_dice=1,DropLowest=False):
    if DropLowest:
        return sum(sorted([sum([random.randint(1,d) for y in xrange(num_dice)])
                           for x in xrange(n)])[1:])
    else:
        return sum([random.randint(1,d) for x in xrange(n)])

def dice_Morgan(n,d):
    total = 0
    while n > 0:
        r = random.randint(2,d)
##        print r
        n -= 1
        if r == 2:
            total += random.randint(1,d)
##            print "Reroll once"
        else:
            total += r
    return total

def d20min10(advantage=False):
    if advantage:
        return sorted([max([random.randint(1,20),10]),max([random.randint(1,20),10])])[-1]
    else:
        return max([random.randint(1,20),10])

def PickBestChargen(num,dice,add=0,DropLowest=False,samples=1):
    a = [Chargen(num,dice,add,DropLowest) for i in xrange(samples)]
##    print a
    return max(a)

def Chargen(num,dice,add=0,DropLowest=False):
    a = [d(num,dice,DropLowest)+add for i in xrange(6)]
    b = [prob_list[n] for n in a]
##    print a,b,sum(b)
    return sum(b)

def rand_low_weight(m, n):
    '''Picks a random number from a half-triangular distribution
from m to n, inclusive, with the weight towards the low end.'''
    # Pick from random.triangular, a full triangular distribution
    temp = int(random.triangular(m,n*2-m))
    # "Fold" the full triangle in half, so the probability
    # distribution goes from low-chance at m and stops at
    # high chance at n
    if temp > n: temp = n*2-temp+1
    # Flip the triangle so that the high chance is near m
    # and the low chance is near n
    return n-temp+m

def print_graph(dmg_list, brief=True, scale=1):
    for i in xrange(min(dmg_list),max(dmg_list)+1):
        c = dmg_list.count(i) // scale
        if not brief:
            display = "I"*c
        elif dmg_list.count(i):
            display = c
        else:
            display = ""
        print "{0} ({1}):\t{2}".format(i,dmg_list.count(i),display)

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

results = []
samples = 1000000
for n in xrange(samples):
    if n % (samples / 10) == 0:
        print n
    results.append(rand_low_weight(1,5))
##    print ""
##r = list(set(results))
##r.sort()
##print results
##print r
print_graph(results, False, 5000)
print_stats([x for x in results if x != 0])
##for i in r:
##    print "{0: 3} ({1: 5}): {2}".format(i, results.count(i), "I"*(results.count(i)/10))
