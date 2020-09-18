"""
A frog is on one side of a river, and it is trying to get to the other side
There are N - 1 lily pads between the frog and the other bank
The frog will randomly choose any of the lilypads in front of him or
the opposing bank (N choices), and hop to whatever he chooses.
He then repeats the process, randomly choosing any spot in front of him
until he gets to the other side.
"""

from random import randint
from math import log

TOTAL_SPOTS = 3
ITERATIONS = 1e7

# For the current total N, reduce the total by a random number between
# 1 and N. Repeat until N=0

totals = []
for i in range(int(ITERATIONS)):
    if (i + 1) % 100000 == 0:
        print("{} / {}".format(i + 1, int(ITERATIONS)))
    N = TOTAL_SPOTS
    total_hops = 0
    while N > 0:
        total_hops += 1
        N -= randint(1, N)
    totals.append(total_hops)

print('')
print(sum(totals) / float(len(totals)))
print(log(TOTAL_SPOTS, 2))