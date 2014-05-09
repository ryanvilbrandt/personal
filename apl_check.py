import math

def GetEmptySlotVal():
    return 5

def CalcAPL(seq):
    total = 0
    for i in xrange(6):
        if len(seq) <= i:
            total += GetEmptySlotVal()
        else:
            total += seq[i]
    print total/6.0, seq

def CalcXP(seq):
    total = 0
    for p in seq:
        if p >= 86:
            total += (p-85)*25+681
        elif p >= 76:
            total += (p-75)*17+511
        elif p >= 66:
            total += (p-65)*14+371
        elif p >= 56:
            total += (p-55)*11+261
        elif p >= 46:
            total += (p-45)*9+171
        elif p >= 36:
            total += (p-35)*7+101
        elif p >= 26:
            total += (p-25)*5+51
        elif p >= 21:
            total += (p-20)*4+31
        elif p >= 16:
            total += (p-15)*3+16
        elif p >= 11:
            total += (p-10)*2+6
        else:
            total += (p-5)*1+1
    print total-1, seq

def CalcLevelFromXP(xp):
    total = 0
    if xp > 1056:
        total = 100
    elif xp > 681:
        total = int((xp-681)/25)+85
    elif xp > 511:
        total = int((xp-511)/17)+75
    elif xp > 371:
        total = int((xp-371)/14)+65
    elif xp > 261:
        total = int((xp-261)/11)+55
    elif xp > 171:
        total = int((xp-171)/9)+45
    elif xp > 101:
        total = int((xp-101)/7)+35
    elif xp > 51:
        total = int((xp-51)/5)+25
    elif xp > 31:
        total = int((xp-31)/4)+20
    elif xp > 16:
        total = int((xp-16)/3)+15
    elif xp > 6:
        total = int((xp-6)/2)+10
    elif xp > 0:
        total = int((xp-1)/1)+5
    else:
        total = 5
    print "{0} ({1})".format(total, xp)

CalcXP([11,11])
CalcLevelFromXP(15+5.5)
CalcLevelFromXP((15+5.5)/6)
##CalcLevelFromXP(680)
##CalcLevelFromXP(681)
##CalcLevelFromXP(704)
##CalcLevelFromXP(705)
##CalcLevelFromXP(706)
##CalcLevelFromXP(1054)
##CalcLevelFromXP(1055)
##CalcLevelFromXP(1056)
##CalcXP([30])
##CalcXP([30,10])
##CalcXP([20,15,10])
##CalcXP([45])
##CalcXP([20,17,20,5])
##CalcXP([12,12,12,13])
##CalcXP([45,39,38,30,25,15])
##CalcXP([100])
##CalcXP([46,46,46,46,46,46])
##CalcXP([15])
##CalcXP([7,7,7,7,6,6])
##CalcXP([15,7])
