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

def calc_prob(num_dice, diff, dice_list=[], ones_cancel=True):
    '''
    @param int num_dice: The number of dice (d10) to simulate, 1 or greater
    @param int diff: The difficulty of the check, from 2 to 10
    @param list(int) dice_list: The list of dice results to check for success or fail

    Recursively creates every possible combination of dice rolls, at the given number of dice.
    Then analyzes each combination as a success, failure, or botch.
    Returns the percentage of how many of those dice combinations were success/fail/botch.
    '''
    if num_dice == 0:
        # If all the dice have been generated, run the roll through the checking
        # function to get the number of successes in that roll.
        r = check_roll(dice_list, diff, ones_cancel)     # 1 if success, 0 otherwise
        return min(1, max(0, r))    # success
##        return 1-min(1, max(0, r))  # fail
##        return min(1, max(0, -r))   # botch
    else:
        
        return float(
            sum(
                [calc_prob(
                    num_dice-1,
                    diff,
                    dice_list+[i],
                    ones_cancel
                    ) for i in xrange(1,11)]
                )
            )/10

def calc_prob_alt(num_dice, diff, succ_count=0):
    if num_dice == 0:
##        return (1 if succ_count >= 5 else 0)  # 1 if 5 successes, 0 otherwise
##        return (1 if succ_count >= 1 else 0)  # 1 if success, 0 otherwise
##        return (1 if succ_count <= 0 else 0)  # 1 if fail, 0 otherwise
        return (1 if succ_count == 0 else 0)   # 1 if botch, 0 otherwise
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

##def algebra_dice(num_dice, successes=1, diff=8, explode=11, die_type=10, ones_cancel=False):
##    # Calculate, on average, how many times a single die will be rolled
##    # when taking 10-agains, 9-agains, and 8-agains into account.
##    # http://axiscity.hexamon.net/users/isomage/rpgmath/explode/
##    # Set explode = die_type+1 to disable exploding dice
##    rolls_per_die = die_type/float(explode-1)
##    single_die_succ_chance = 1-(float(diff-1)/die_type)
##    single_die_fail_chance = (float(diff-1)/die_type)
##    # To handle multiple successes, we first find the chance that
##    # successes-1 dice will ALL come up successes.
##    required_prob = single_die_succ_chance**((successes-1)*rolls_per_die)
##    # We then find the chance the that remaining dice will come
##    # up with at least one success.
##    optional_prob = 1-(single_die_fail_chance**((num_dice-successes+1)*rolls_per_die))
##    return max(0, required_prob*optional_prob)

def algebra_dice(num_dice, successes=1, diff=8, explode=10, die_type=10, ones_cancel=False):
    return (3*num_dice)/(explode-1)

def RollnWoD(num_dice, diff=8, again=10, die_type=10):
    i = 0
    total = 0
    while i < num_dice:
        r = random.randint(1, die_type)
        if r >= diff:
            total += 1
        if r < again:
            i += 1
    # returns total number of successes
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


successes = 1
# Set to 11 to disable exploding dice
explode = 10

print "Algebraic method:"
for dice in xrange(1, 11):
    a = algebra_dice(dice, successes=successes, explode=explode)
    print "{:.2%}\t".format(a),
print

print

iters = 100000
print "{:,} simulations:".format(iters)
for num_dice in xrange(1, 11):
    success_count = 0
    for _ in xrange(iters):
        success_count += (1 if (RollnWoD(num_dice, again=explode) >= successes) else 0)
    print "{:.2%}\t".format(success_count/float(iters)),
print

##print_stats(a)
##print_graph(a,False,250)




