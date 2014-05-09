import time

def rec_fact(n):
    """returns the factorial of n"""
    if n == 0:
        return 1
    else:
        return n * rec_fact(n-1)

def iter_fact(n):
    r = 1
    for x in range(1,n+1):
        r *= x
    return r

n = 800
t = time.clock()
r = rec_fact(n)
print time.clock()-t
print r
print ""
t = time.clock()
r = iter_fact(n)
print time.clock()-t
print r
