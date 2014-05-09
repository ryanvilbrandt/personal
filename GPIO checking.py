import fnmatch, os, re

match = "*.csv"

matches = []
for root, dirnames, filenames in os.walk('.'):
  for filename in fnmatch.filter(filenames, match):
      matches.append(os.path.join(root, filename).replace('\\','/'))

##matches = ["./Key 012/V3 Am Alive 4.5.6 Test Result Log.csv"]
##bounds = [(10.8, 12.5), (8.8, 10.5), (0, 0.5), (11.3, 12.5)]

bad_set = set()
full_set = set()
bad_dict = {}

for path in matches:
##    print "Searching {0} now".format(path)
    with open(path, 'r') as f:
        for line in f.readlines():
##            print line
            m = re.search(r"Program and Check the GPS ID,\d+,Pass,0.0,(\d+)", line)
            if m:
                gpsid = m.group(1)
                full_set.add(gpsid)
                mall = re.findall(r"Check Gpio (\d) Status,\d+,(Pass|Fail),0.0,A: (.*?)V  /  B: (.*?)V  /  C: (.*?)V  /  D: (.*?)V", line)
                if mall:
                    bad_dict[gpsid] = 0
                    for m in mall:
                        try:
                            if ((10.8 > float(m[2]) or float(m[2]) > 12.5) or
                                (8.8 > float(m[3]) or float(m[3]) > 10.5) or
                                (0 > float(m[4]) or float(m[4]) > 0.5) or
                                (11.3 > float(m[5]) or float(m[5]) > 12.5)):
##                            if ((9.0 > float(m[2]) or float(m[2]) > 14.5) or
##                                (6.0 > float(m[3]) or float(m[3]) > 12.5) or
##                                (0 > float(m[4]) or float(m[4]) > 2.5) or
##                                (10.0 > float(m[5]) or float(m[5]) > 14.5)):
##                            if (float(m[2]) == 0.0 or
##                                float(m[3]) == 0.0 or
##                                float(m[5]) == 0.0):
##                                print "{0} GPIO {1}: {2}".format(gpsid, m[0], m[2:])
                                if 00000000 <= int(gpsid) <= 7999999:
                                    print ",".join(m[2:])
                                bad_set.add(gpsid)
                                bad_dict[gpsid] += 1
                        except Exception as e:
                            print "Error with {0} GPIO {1}: {2}".format(gpsid, m[0], e)
##    print ""

##for k in bad_dict.copy():
##    if bad_dict[k] == 0:
##        del bad_dict[k]
##
##print "GPSIDs of units with out-of-bounds GPIO tests"
##print bad_set
##print ""
##print "Number of units with out-of-bounds GPIO tests:",len(bad_set)
##print "Number of total units:",len(full_set)
##print "Percent of total units with out-of-bounds GPIO tests: {0:2%}".format(float(len(bad_set))/len(full_set))
##print ""
##print "Suntron V3:"
##for k in sorted(bad_dict):
##    if 8000000 <= int(k) <= 8499999:
##        print "{0}: {1}".format(k, bad_dict[k])
##print ""
##print "Keytronic V3:"
##for k in sorted(bad_dict):
##    if 8500000 <= int(k) <= 8999999:
##        print "{0}: {1}".format(k, bad_dict[k])
##print ""
##print "VT HU:"
##for k in sorted(bad_dict):
##    if int(k) >= 11000000:
##        print "{0}: {1}".format(k, bad_dict[k])
##print ""
##print "V3R:"
##for k in sorted(bad_dict):
##    if int(k) <= 8000000:
##        print "{0}: {1}".format(k, bad_dict[k])


