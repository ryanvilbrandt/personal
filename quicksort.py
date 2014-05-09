def comp(a,b,key=None):
    if key:
        if key(a) < key(b):
            return -1
        elif key(a) == key(b):
            return 0
        else:
            return 1
    else:
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1

def get_median3(a,b,c):
    if b <= a and b >= c: return b
    if a <= b and a >= c: return a
    return c

def Quicksort(seq, key=None):
    if len(seq) < 2:
        return seq
    elif len(seq) < 3:
        if comp(seq[0],seq[-1],key):
            return seq
        else:
            return [seq[-1],seq[0]]
    else:
        # Get index of the median value of the first, middle, and last.
        i = int(len(seq)/2)
        if seq[i] <= seq[0] and seq[i] >= seq[-1]:
            pivot = i
        elif seq[0] <= seq[i] and seq[0] >= seq[-1]:
            pivot = 0
        else:
            pivot = -1
        seq_less = []
        seq_more = []
        p = seq[pivot]
        for i,n in enumerate(seq):
            if i != pivot:
                if comp(n,p,key):
                    seq_less.append(n)
                else:
                    seq_more.append(n)
        return Quicksort(seq_less, key) + [p] + Quicksort(seq_more, key)

def SwapSort(seq, key=None):
    swap_done = True
    while(swap_done):
        swap_done = False
        for i in xrange(len(seq)-1):
            if comp(seq[i],seq[i+1],key) == 1:
                seq[i+1], seq[i] = seq[i], seq[i+1]
                swap_done = True
                break

    return seq
    


if __name__ == "__main__":
    import random, time, gc
    gc.disable()
    r = [random.randint(1,1000) for i in xrange(5000)]
    t = time.clock()
    Quicksort(r)
    print "Time to quicksort:",time.clock()-t
    gc.collect()
    t = time.clock()
    SwapSort(r)
    print "Time to SwapSort:",time.clock()-t
    gc.collect()
    t = time.clock()
    r = sorted(r)
    print "Time to built-in sort:",time.clock()-t
        
