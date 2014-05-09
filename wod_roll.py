import random, time, gc

def check_roll(l, diff, ones_cancel=True):
    succ = 0
    for n in l:
        if n >= diff:
            succ += 1
        elif n == 1 and ones_cancel:
            succ -= 1
    return succ

def check_roll_no_ones(l, diff):
    succ = 0
    ones = 0
    for n in l:
        if n >= diff:
            succ += 1
        elif n == 1:
            ones += 1
    if succ:
        return succ
    return -ones

def roll_dice(num_dice, diff, iterations=100000):
    count = 0
    for n in xrange(iterations):
        if check_roll([random.randint(1,10) for i in xrange(num_dice)],
##                      diff) >= 5:   # If the roll has 5+ successes
                      diff) > 0:    # If the roll is a success
##                      diff) == 0:   # If the roll is a fail
##                      diff) < 0:    # If the roll is a botch
            count += 1
    return float(count)/iterations

def roll_dice_no_ones(num_dice, diff, iterations=100000):
    count = 0
    for n in xrange(iterations):
        if check_roll_no_ones([random.randint(1,10) for i in xrange(num_dice)],
##                      diff) >= 5:   # If the roll has 5+ successes
                      diff) > 0:    # If the roll is a success
##                      diff) == 0:   # If the roll is a fail
##                      diff) < 0:    # If the roll is a botch
            count += 1
    return float(count)/iterations

def calc_prob(num_dice, diff, l=[]):
    if num_dice == 0:
        r = check_roll(l, diff)     # 1 if success, 0 otherwise
##        return min(1, max(0, r))    # success
##        return 1-min(1, max(0, r))  # fail
        return min(1, max(0, -r))   # botch
    else:
        return float(sum([calc_prob(num_dice-1,diff,l+[i])
                          for i in xrange(1,11)]))/10

def calc_prob_alt(num_dice, diff, succ_count=0):
    if num_dice == 0:
##        return min(5, max(4, succ_count))-4 # 1 if 5 successes, 0 otherwise
##        return min(1, max(0, succ_count))   # 1 if success, 0 otherwise
##        return 1-min(1, max(0, succ_count)) # 1 if fail, 0 otherwise
        return min(1, max(0, -succ_count))  # 1 if botch, 0 otherwise
    else:
        l = []
        for i in xrange(1,11):
            if i >= diff:
                l.append(calc_prob_alt(num_dice-1,diff,succ_count+1))
            elif i == 1:
                l.append(calc_prob_alt(num_dice-1,diff,succ_count-1))
            else:
                l.append(calc_prob_alt(num_dice-1,diff,succ_count))
        return float(sum(l))/10

def calc_prob_no_ones(num_dice, diff, succ_count=0, ones_count=0):
    if num_dice == 0:
##        return min(5, max(4, succ_count))-4 # 1 if 5 successes, 0 otherwise
        return min(1, max(0, succ_count))   # 1 if success, 0 otherwise
##        return 1-min(1, max(0, succ_count)) # 1 if fail, 0 otherwise
##        if succ_count == 0:     # 1 if botch, 0 otherwise
##            return min(1,ones_count)
##        return 0
    else:
        l = []
        for i in xrange(1,11):
            if i >= diff:
                l.append(calc_prob_no_ones(num_dice-1,diff,succ_count+1,ones_count))
            elif i == 1:
                l.append(calc_prob_no_ones(num_dice-1,diff,succ_count,ones_count+1))
            else:
                l.append(calc_prob_no_ones(num_dice-1,diff,succ_count,ones_count))
        return float(sum(l))/10

def RollnWoD(n, diff=8, again=10):
    i = 0
    total = 0
    a = []
    while i < n:
##        print n,diff,i,total
        r = random.randint(1,10)
        a.append(r)
        if r >= diff:
            total += 1
        if r < again:
            i += 1
##    print a
    return total

def print_graph(seq, brief=True, scale=1):
    graph_column_start = len(str(len(seq))) + len(str(max(seq))) + 4
    for i in xrange(min(seq),max(seq)+1):
        c = seq.count(i) // scale
        if not brief:
            display = "I"*c
        elif seq.count(i):
            display = c
        else:
            display = ""
        header = "{0} ({1}):".format(i,seq.count(i))
        print "{0}{1}{2}".format(header,
                                 " "*(graph_column_start-len(header)),
                                 display)

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


a = []
for i in xrange(100000):
    a.append(RollnWoD(4+6+2+3))

print_stats(a)
print_graph(a,False,250)




