import random

s=8+5
dc=20
# price in sp
price=1500
interval = "Week"

take_ten = True
time = 0
prog = 0
cost = price / 3.0
print "Creating {0}gp item at {1} DC at {2} skill".format(price/10,dc,s)
print "Hit Enter to continue, type anything to stop"
while(raw_input()==""):
    if take_ten:
        d = 10
    else:
        d = random.randint(1,20)
    
    print "{0}+{1}={2} vs DC {3}".format(d,s,d+s,dc)
    result = d+s
    if result <= dc - 5:
        temp = price / 6.0
        cost += temp
    elif result >= dc:
        temp = result*dc
        if interval == "Day":
            temp = temp / 7.0
        prog += temp
    time += 1
    print "{5} {0}: {1:.2f}gp / {2}gp ({3:.2%}) -- Cost {4:.2f}gp".format(time,prog/10.0,price/10,
                                                                          float(prog)/price,cost,interval)
    if prog >= price:
        effic = price/float(prog)
        print "Done! At {0:.2f}gp out of {1}gp. (Total time={2:.2f} {3}s)".format(prog/10.0,price/10,effic*time,interval)
        break
