##with open("debug.txt") as f_in:
##    with open("debug_out.txt", 'w') as f_out:
##        for line in f_in:
##            if line.startswith("Average reading:") or line.startswith("Test 42"):
##                f_out.write(line)


f_in = open("debug_out.txt")
with open("debug_out.csv", 'w') as f_out:
    try:
        while True:
            time_line = f_in.readline()
            t = time_line.split(' ')
            data_line = f_in.readline()
            d = data_line.split(' ')
            f_out.write("{} {} {},{},\n".format(t[4], t[5], t[6], d[8]))
    except Exception as e:
        print(e)
f_in.close()
