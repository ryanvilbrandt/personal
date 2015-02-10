import sys

def print_array(a, digits=3):
    for i in a:
        print "|",
        for j in i:
            print "{0:^1}".format(j),
        print "|"

def build_primes(max_n):
    r = range(2,max_n)
    proved_primes = []
    for i in r:
        proved = True
        for j in proved_primes:
            if i % j == 0:
                proved = False
        if proved:
            proved_primes.append(i)
    return proved_primes

def sieve(N):
    # Open primes_list.txt, if it exists
    try:
        with open("primes_list.txt", 'r') as f:
            primes = eval(f.read())
    except Exception:
        primes = []
    # Check if more primes need to be calculated
    if not primes or max(primes) < N:
        print "Building primes list"
        if primes:
            # Create number list starting AFTER the highest prime in primes
            nums = range(max(primes)+1, N)
        else:
            # Create number list starting at 2
            nums = range(2, N)
        # Sieve of Eratosthenes
        for i in range(2, int(N**0.5)+1): 
            nums = filter(lambda x: x == i or x % i, nums)

        # Write new set of primes to primes_list.txt
        with open("primes_list.txt", 'w') as f:
            f.write(repr(primes + nums))
        return primes + nums
    else:
        return primes

def ifprime(n, fast=True):
    '''
    Fast mode only works on an ordered list of primes, and when
    n is increasing incrementally with each call.
    '''
    global prime_numbers
    if fast:
        if prime_numbers and n == prime_numbers[0]:
            prime_numbers = prime_numbers[1:]
            return "X"
    else:
        if n in prime_numbers:
            prime_numbers.pop(n)
            return "X"
    return " "

def build_spiral(array_size):
    global prime_numbers
    a = []
    for i in xrange(array_size):
        a.append([" "]*array_size)


    prime_numbers = sieve(array_size**2)

    center = (array_size)/2
    x = center
    y = center
    a[center][center] = 1
    layer = 1
    count = 2
    for i in xrange(1,center+1):
        print layer
        layer = i
        length = layer*2-1
        start_x = center+layer-1
        start_y = center+max(0,layer-2)
##        print layer,length,start_x,start_y
        x = start_x
        y = start_y
        for j in xrange(length-1):
            a[y-j][x] = ifprime(count)
            count += 1
        y -= length-2
        for j in xrange(1,length):
            a[y][x-j] = ifprime(count)
            count += 1
        x -= length-1
        for j in xrange(1,length):
            a[y+j][x] = ifprime(count)
            count += 1
        y += length-1
        for j in xrange(1,length):
            a[y][x+j] = ifprime(count)
            count += 1
        x += length-1

    return a

def build_topdown_spiral(array_size):
    layer = array_size/2
    dfc = layer-1
    build_spiral_recur(layer,dfc)
    build_spiral_recur(layer,dfc-1)
    print layer, 4*(layer**2)-8*layer+5

def build_spiral_recur(layer,dfc):
    if abs(dfc) == layer - 1:
        pass
    
if __name__ == "__main__":
    array_size = 9
##    a = build_topdown_spiral(array_size)
    a = build_spiral(array_size)
    print_array(a)

