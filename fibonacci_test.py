from math import sqrt

SQRT_5 = sqrt(5)
PHI_PLUS = (1+SQRT_5)/2
PHI_MINUS = (1-SQRT_5)/2

def fib(n, start=1, start_last=0):
    last = start_last
    current = start
    for i in xrange(n-1):
        total = last + current
        last = current
        current = total
    return current

def fib2(n):
    return (PHI_PLUS**n - PHI_MINUS**n)/SQRT_5

print "Using the math equation:"
print fib2(10000)
