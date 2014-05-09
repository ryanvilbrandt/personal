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


n = 10

##print calc_prob_alt(1,2)

gc.disable()
t = time.clock()
for i in xrange(8,11):  # Number of dice
    print "|-"
    print "!{0}*".format(i)
    for j in xrange(2,11):  # Difficulty
##        r = roll_dice(i,j)
        r = roll_dice_no_ones(i,j)
##        r = calc_prob_alt(i,j)
##        r = calc_prob_no_ones(i,j)
        print '| style="text-align: right;"|{0:.2%}'.format(r)
    gc.collect()
print time.clock()-t
gc.enable()
