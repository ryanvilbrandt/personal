from math import pi

# Equation from http://mathforum.org/library/drmath/view/63839.html

while(True):
    outd = input("Outer diameter? ")
    ##outd = 4.5185
    ind = input("Inner diameter? ")
    ##ind = 2.4025
    reeltype = input("Type?\n1: Black reel (0.0540 in, 18 parts/2.7960 in)"+
                     "\n2: R&C reel (0.0415 in, 29 parts/4.5445 in)"+
                     "\n3: Custom\n? ")
    if (reeltype == 1): # Black reel
        t = 0.0540
        p = 18/2.7960
    elif (reeltype == 2): # R&C reel
        t = 0.0415
        p = 29/4.5445
    else:
        t = input("Thickness? ")
        p = input("Parts per unit length? ")
        

    a = ind/2.0 - t
    n = float(outd-ind)/2/t
    a = 2.0*pi*a*n + 2.0*pi*t*(n+1)*n/2.0
    print a*p
    print ""
