import operator

card_types = [3,4,5,6,7,8,9,10,11,12,13,50]

# Checks for group of three or more identical cards in hand
# Returns True only if no group is found
def CheckForNoSolution(hand, wild=0, limit=3):
    d = {}
    for c in hand:
        # If card is a wild, increment count of all cards in dictionary
        # Otherwise, only the current card
        if c == 50 or c == wild:
            seq = card_types
        else:
            seq = [c]
        for value in seq:
            # Get card from counting dictionary. If doesn't exist, pass count of 0
            count = d.get(value, 0)
            # Increment count in dictionary by 1. If would be limit or greater, fail test
            if count+1 >= limit:
                return False
            d[value] = count + 1
    return True

def ScoreHand(hand):
    return sum(hand)

def BuildHand(hand=[], hand_size=0, wild_card=0, cards=[]):
    global possibilities
    # First, check that the hand-in-progress has no solution (runs/sets)
    if CheckForNoSolution(hand, wild=wild_card):
        # If hand has no solution and is the desired hand size, score the hand
        if hand_size == 0:
            possibilities[str(hand)] = ScoreHand(hand)
        else:        
            # Otherwise, continue adding appropriate cards
            for i,c in enumerate(cards):
                # Only allow any further cards from current card and up
                # This enforces unique hands, and drastically lessens the number of cycles necessary
                BuildHand(hand+[c], hand_size-1, wild_card, cards[i:])

# Brute force all the possible hands, and print the hand and score of the ten highest
for HandSize in xrange(3,14):
    possibilities = {}
    print "\nFor hand size {0}:".format(HandSize)
    BuildHand(hand_size=HandSize, wild_card=HandSize, cards=card_types)
    sorted_dict = sorted(possibilities.iteritems(), key=operator.itemgetter(1))
    for x in sorted_dict[-10:]:
        print x[0],x[1]
    mean = 0
    median = 0
    mode = (0,0)
    mode_count = 0
    current_mode = 0
    for i,x in enumerate(sorted_dict):
        mean += x[1]
        if i == len(sorted_dict)/2:
            median = x[1]
        if x[1] != current_mode:
            current_mode = x[1]
            mode_count = 1
        else:
            mode_count += 1
        if mode_count >= mode[1]:
            mode = current_mode,mode_count
    print "Mean:",float(mean)/len(sorted_dict)
    print "Median:",median
    print "Mode:",mode
