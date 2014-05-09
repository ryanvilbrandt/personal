#!/usr/bin/env python
import random

def d(n,d):
    t = [random.randint(1,d) for x in xrange(n)]
##    print t
    return sum(t)

def dice(n,d,explode=[]):
    i = 0
    t = []
    while i < n:
        t.append(random.randint(1,d))
        if not (t[-1] in explode):
            i += 1
    return t

##for n in range(10):
##    print d(5,6)*10
##    print d(3,6), d(3,6), d(3,6), d(3,6), d(3,6), d(3,6)

##for V5 in xrange(1,21):
##    print int((V5+1)/2)

##for i in xrange(1,10):
##    print 2*i-1

print d(5,6)*10
