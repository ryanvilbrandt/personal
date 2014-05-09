import itertools
S = 20
N = 4

def BuildBlottoOptions(S, N, cur_list=[]):
    '''Creates a list L of all possible lists of size N,
of non-decreasing positive integers whose sum = S,
ordered from lowest prefixes to highest'''
    # If this is the last bucket in the list, just
    # take whatever resources are left over, and return
    # the whole list
    if N == 1:
        return [cur_list + [(S - sum(cur_list))]]
    # A list of lists that is added onto whenever N == 1
    blotto_list = []
    if cur_list == []:
        i = 1
    else:
        i = cur_list[-1]
    # Range is from 1 or the last value in cur_list,
    # to the remaining resources (S-sum()) divided by
    # the remaining buckets (N)
    for n in xrange(i, int((S-sum(cur_list))/N)+1):
        L = cur_list[:]
        L.append(n)
        blotto_list += BuildBlottoOptions(S, N-1, L)
    return blotto_list

def score_blotto_list(b, r=None):
    b2 = b[:]
    d = {}
    if r == None:
        list_range = range(len(b))
    elif not isinstance(r, list):
        print "Invalid value for r. Must be None or list"
        return None
    else:
        list_range = r
    for c in list_range:
        if c >= len(b):
            break
        m = b[c]
        if c % 100 == 0:
            print "{0} / {1}".format(c, len(list_range))
        total_score = 0
        for n in b2:
            score = comp_score(m,n)
            if score > 0:
                total_score += 1
            if score < 0:
                total_score -= 1
    ##        print m,n,score,total_score
        d[str(m)] = total_score
    return d,sorted(d, key=d.get, reverse=True)

def comp_score(m, n):
    total_score = 0
    for p in set(itertools.permutations(n)):
        score = 0
        for i,x in enumerate(m):
            if m[i] > p[i]:
                score += 1
            elif m[i] < p[i]:
                score -= 1
        if score > 0:
            total_score += 1
        elif score < 0:
            total_score -= 1
    return total_score

def old_comp_score(m, n):
    score = 0
    for i,x in enumerate(m):
        if m[i] > n[i]:
            score += 1
        elif m[i] < n[i]:
            score -= 1
    return score
    

b = BuildBlottoOptions(S,N)
if b == []:
    print "No valid strategies for that input"
else:
    print "Blotto built. Sorting now..."
    # Sort using our custom compare function
    b = sorted(b, cmp=comp_score, reverse=True)
    print "Sort done. Printing to output.txt now..."
    with open("output.txt", "w") as f:
        f.write("Top strategies:\n")
        print_format = "{0:>3} {1:.2%} {2}"
        d,L = score_blotto_list(b)
        for x in L:
            out = print_format.format(d[x], float(d[x])/len(b), x)
##            print out
            f.write(out+"\n")

##        f.write("\n\nTop 100 strategies against each other:\n")
##        b = L[:100]
##        d,L = score_blotto_list(b)
##        for x in L:
##            out = print_format.format(d[x], float(d[x])/len(b), x)
####            print out
##            f.write(out+"\n")
            
##        f.write("\n\nAll strategies, from most successful to least successful:\n")
##        f.write("\n".join([str(x) for x in b]))
            

    print "Done."

    ##print "Blotto built to output.txt. Comparing now..."
    ##print "{0} strategies to compare".format(len(b))
    ##d = score_blotto_list(b)
    ##
    ##print "Compare done, writing to output.txt now..."
    ##
    ##print_format = "{0:<10} {1:>3} {2:.2%}"
    ##for i in xrange(min(len(r),10)):
    ##    print print_format.format(x, d[x], float(d[x])/len(d))
    ##
    ##try:
    ##    f = open("output.txt", "a")
    ##except Exception as e:
    ##    print e
    ##else:
    ##    for x in r:
    ##        f.write((print_format+"\n").format(x, d[x], float(d[x])/len(d)))
    ##finally:
    ##    f.close()
    ##
    ##print "Done."

