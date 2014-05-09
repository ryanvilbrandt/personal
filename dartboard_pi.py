from random import random

# Pretend we have a square board of length D,
# with a circle inside it of diameter D.
# Pick thousands of random points within the square
# Then determine how many of those points fall within the circle
# The ratio of points in the circle to total points = pi/D


##D = 10000000000000.0
##r = D/2.0
total = 100000000
count = 0.0

try:
    for i in xrange(total):
        if i % 1000000 == 0:
            print "{0} / {1} ({2:.0%})".format(i,total,float(i)/total)
        x = random()
        y = random()
        if x**2 + y**2 <= 1:
            count += 1.0
    ##    print x, y, r**2, x**2 + y**2, count
except KeyboardInterrupt:
    print "Break on",i
else:
    print count
    print total
    print count/total*4
