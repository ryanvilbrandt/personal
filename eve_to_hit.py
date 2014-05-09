import sys

def chance_to_hit(trans_speed, sig_res, sig_rad, range_to,
                  track_speed, optimal, falloff):
    sig_eq = (float(trans_speed)/(range_to * track_speed)) * (float(sig_res)/sig_rad)
    range_eq = float(max(0,range_to-optimal))/falloff
    return 0.5**((sig_eq)**2 + (range_eq)**2)

# Range from 5 km to 150km
distance_range = range(500,150500,500)

def best_of_range(trans_speed, sig_rad, sig_res, track_speed, optimal, falloff):
    ideal_distance = 0
    max_chance = 0
    for d in distance_range:
        chance = chance_to_hit(trans_speed, sig_res, sig_rad, d,
                               track_speed, optimal, falloff)
##        print d, chance
        if chance >= max_chance:
            max_chance = chance
            ideal_distance = d
            
    return ideal_distance, max_chance

# The list of signature radiuses to test against
signature_radius_range = [30, 45, 65, 90, 130, 150]
# The range of transversal speeds in m/s
# Starts from arg1 and stops just before ar2, in steps of arg3
trans_speed = range(0, 1550, 50)

optimal = 10000
falloff = 17000
##signature_resolution = 40   # Small
signature_resolution = 125  # Medium
##signature_resolution = 400  # Large
tracking_speed = 0.34

print "Optimal range: {0}km".format(optimal/1000.0)
print "Falloff range: {0}km".format(falloff/1000.0)
print "Signature resolution: {0}m".format(signature_resolution)
print "Tracking speed: {0}rad/sec".format(tracking_speed)
print ""
column_width = 18
width = len(signature_radius_range)*(column_width+1)-1
fmt = "Transversal|{0:^"+str(width)+"}|"
print fmt.format("Signature radius")
fmt = "{0:^"+str(column_width)+"}"
print " velocity  |" + "|".join([fmt.format(r) for r in signature_radius_range]) + "|"
##best = best_of_range(0, 30,
##                     signature_resolution,
##                     tracking_speed,
##                     optimal, falloff)
for speed in trans_speed:
    sys.stdout.write("{0:^11}".format(speed)+"|")
    for r in signature_radius_range:
        best = best_of_range(speed, r,
                             signature_resolution,
                             tracking_speed,
                             optimal, falloff)
        f = "{0}km ({1:.2%})".format(best[0]/1000.0, best[1])
        fmt = fmt = " {0:^"+str(column_width-2)+"} "
        sys.stdout.write(fmt.format(f)+"|")
    print ""





