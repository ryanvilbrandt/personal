import time, gc
from math import sqrt
from itertools import islice

def sieve(N, use_file=True, filename="primes_list.txt"):
    # Open primes_list.txt, if it exists
    primes = [2, 3]
    if use_file:
        try:
            with open(filename, 'r') as f:
                primes = eval(f.read())
        except Exception:
            pass
    # Check if more primes need to be calculated
    if not primes or max(primes) < N:
        print("Building primes list")
        if primes:
            # Create number list starting AFTER the highest prime in primes
            nums = range(max(primes) + 1, N + 1, 2)
        else:
            # Create number list starting at 2
            nums = [2] + range(3, N + 1, 2)
        # Sieve of Eratosthenes
        for i in [2] + range(3, int(N**0.5) + 1, 2):
            if i % (N / 100) == 0: print(i)
            nums = filter(lambda x: x == i or x % i, nums)

        if use_file:
            # Write new set of primes to primes_list.txt
            with open(filename, 'w') as f:
                f.write(repr(primes + nums))
        return primes + nums
    else:
        return primes

# Uses Newton's method to approximate an integer square root
# From http://stackoverflow.com/questions/15390807/integer-square-root-in-python
def isqrt(n, y=None):
    x = n
    if y is None:
        y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def increment_check(N, use_file=True, filename="primes_list.txt"):
    # Open primes_list.txt, if it exists
    primes = [2, 3]
    if use_file:
        try:
            with open(filename, 'r') as f:
                primes = eval(f.read())
        except Exception:
            pass
    # Check if more primes need to be calculated
    if primes[-1] < N:
        print("Building primes list from {:,} to {:,}".format(primes[-1] + 2, N))
        # Cycle through all odd numbers starting with the next highest in the primes list, up to the target N
        sq_root = None
        for curr_number in range(primes[-1] + 2, N + 1, 2):
            sq_root = sqrt(curr_number)
            # Check all current known primes to find if any are factors in the current number
            for n in primes:
                # If n is a factor, the current number is not prime
                if curr_number % n == 0:
                    break
                # If n is greater than the square root of the current number,
                # we've determined that the current number is prime
                if n > sq_root:
                    primes.append(curr_number)
                    break

        if use_file:
            # Write new set of primes to primes_list.txt
            with open(filename, 'w') as f:
                f.write(repr(primes))
        return primes
    else:
        return primes

def build_primes(max_n):
    proved_primes = [2]
    for i in xrange(3, max_n, 2):
        for j in proved_primes:
            if i % j == 0:
                proved = False
                break
        else:
            proved_primes.append(i)
    return proved_primes


if __name__ == "__main__":
    gc.disable()

    # N = [10, 100, 1000, 10000, 100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000]
    # N = [1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000]
    N = xrange(100000, 1000000, 10000)

    # t = time.clock()
    # nums_a = range(2, N)
    # for i in range(2, N):
    #     nums_a = filter(lambda x: x == i or x % i, nums_a)
    # print time.clock() - t
    # # print nums_a
    #
    # t = time.clock()
    # nums_b = build_primes(N)
    # print time.clock() - t
    # # print nums_b

    # t = time.clock()
    # nums_c = increment_check(N)
    # print time.clock() - t
    # # print nums_c
    times = []

    for n in N:
        t = time.clock()
        nums_d = increment_check(n, use_file=False)
        times.append(time.clock() - t)
        gc.collect()

    print(times)

    # print nums_a == nums_b
    # print nums_b == nums_c
    # print nums_c == nums_d


