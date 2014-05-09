import time, re

a = []
num_tests = 37
unit_count = 0
filename = "debug_013_V3R.txt"

print "Building CSV file for {0}...".format(filename)
with open(filename, "r") as f:
    with open("results.csv", "w") as o:
        temp = 40 if num_tests == -1 else num_tests+1
        o.write("\n"*8)
        o.write("Start Time,{0},Total Test Time,\n".format(",".join(["Test {0}".format(i) for i in range(1,temp)])))
        for line in f:
            if line.startswith("Test"):
                m = re.match("Test (\d+) started at (.*)", line)
                if m:
                    try:
                        t = time.mktime(time.strptime(m.group(2), "%m/%d/%Y %I:%M:%S %p"))
                    except ValueError:
                        t = time.mktime(time.strptime(m.group(2), "%d/%m/%Y %I:%M:%S %p"))
                    if m.group(1) == "1":
                        a = [m.group(2)]
                    a.append(t)
            elif line.startswith("Summary:"):
##                print len(a)
                if (line == "Summary: All tests passed\n" and
                    (num_tests == -1 or num_tests+2 == len(a))):
                    total_time = 0
                    for i,x in enumerate(a):
                        if i == 0:
                            o.write(a[0]+",")
                        elif i == 1:
                            pass
                        else:
                            t = a[i]-a[i-1]
                            total_time += t
                            o.write(str(t)+",")
                    o.write(str(total_time)+",\n")
                    unit_count += 1

print "Done. {0} test lists saved".format(unit_count)
