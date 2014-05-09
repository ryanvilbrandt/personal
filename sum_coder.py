import random, math

# Takes a string/list and rearranges it so the first items are in the
# middle and the last items are out near the ends.
def shufflelist(l):
    left = True
    s = ""
    for c in l:
        if left:
            s = c+s
        else:
            s = s+c
        left = not left
    return s

def encodestring(s, clist, base):
    digits = int(math.ceil(len(clist)/float(base-1)))
    if digits >= base:
        return ""
    s = "".join([encodechar(c,clist,digits,base)
                    for c in s.lower()])
    return s + baseN(digits,base) + baseN(base-1,base)

def encodechar(ch, clist, digits, base):
    i = clist.find(ch)
    if i == -1:
        return ""
    s = ""
    for j in range(1,digits):
        x = random.randint(max(0,i-(base-1)*(digits-j)),min(i,(base-1)))
        s += baseN(x,base)
        i -= x
    return s + baseN(i,base)

# baseN function shamelessly modified and ripped from http://dft.ba/-gPl
# Accepts any int for num, and any int from 2 to 36 for b
# numerals must be a string of at least len(b)
def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return (((num < 0) and "-"+baseN(-num, b, numerals)) or
            ((num == 0) and  "0" ) or
            ( baseN(num // b, b, numerals).lstrip("0") + numerals[num % b]))

# int2base function shamelessly ripped from http://dft.ba/-gLs
##def int2base(x, base, digs="0123456789abcdefghijklmnopqrstuvwxyz"):
##  if x < 0: sign = -1
##  elif x==0: return '0'
##  else: sign = 1
##  x *= sign
##  digits = []
##  while x:
##    digits.append(digs[x % base])
##    x /= base
##  if sign < 0:
##    digits.append('-')
##  digits.reverse()
##  return ''.join(digits)

def decodestring(s, clist):
    if not s:
        return ""
    digs="0123456789abcdefghijklmnopqrstuvwxyz"
    base = int(digs.find(s[-1]))+1
    digits = int(s[-2],base)
    s = s[:-2]
    return "".join([decodechar(s[i:i+digits],charlist,base)
                    for i in range(0,len(s),digits)])

def decodechar(c, clist, base):
    return clist[sum([int(x, base) for x in c])]


charlist = " etaonrishdlfcmugypwbvkxjqz.?!,'+-*/=0123456789"
charlist = shufflelist(charlist)
base = 36

instr = raw_input("Input: ")
while(not instr == "quit"):
    z = encodestring(instr, charlist, base)
    print z
    print decodestring(z, charlist)

    instr = raw_input("Input: ")
