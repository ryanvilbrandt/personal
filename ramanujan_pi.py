# Implementation of Ramanujan's formula
# https://crypto.stanford.edu/pbc/notes/pi/ramanujan.html

# 1/pi = sqrt(8)/9801 SUM[n=0 to inf] ( 4n!/(n!)^4 * (26390^n + 1103)/396^(4n)) )

from __future__ import division
from math import factorial, sqrt

a = sqrt(8) / 9801

total = 0
for n in xrange(100):
    total += (factorial((4*n)) / factorial(n)**4) * (26390**n + 1103) / 396**(4 * n)
    print 1 / (a * total)


