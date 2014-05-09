import random

def shuffle_word(w):
    if len(w) > 3:
        temp = w[1:-1]
        while temp == w[1:-1]:
            temp = "".join(random.sample(temp, len(temp)))
        w = w[0] + temp + w[-1]
    return w

def shuffle_sentence(s):
    return " ".join([shuffle_word(w) for w in s.split(" ")])

s = "Baseball players performing similarly absolutely deserve comparable treatment"
print shuffle_sentence(s)

##instr = raw_input("Input: ")
##while(not instr == "quit"):
##    print " ".join([shuffle_word(w) for w in instr.split(" ")])
##
##    instr = raw_input("Input: ")
