import time, gc

gc.disable()

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


N = 100

t = time.clock()
nums = range(2, N**2-1) 
for i in range(2, N): 
    nums = filter(lambda x: x == i or x % i, nums)

##print nums
print time.clock()-t

t = time.clock()
p = build_primes(N**2-1)
print time.clock()-t


