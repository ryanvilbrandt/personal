import random

# Out of 1,000,000 rolls on a single die, how often I'll get 0, 1, 2, 3... successes
LIST_NO_EXPLODE = []

iterations = 100000
DIE = 10
AGAIN = 8  # Dice explodes at this number and above. Set it to DIE+1 for nonexploding
results = []

def roll(d=DIE, again=AGAIN):
    r = random.randint(1, d)
    if r >= again:
        r += roll(d, again)
    return r

def die_success_chance

for i in xrange(iterations):
    results.append(roll())

# print results
print sum(results)/float(len(results))

k = 1+DIE-AGAIN
print ((DIE+1)/2.0) * DIE/(DIE-k)