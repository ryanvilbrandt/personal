import re, csv

DELIMITER = ','
input_filename = "4.7.5 8031595.csv"
output_filename = "4.7.5 8031595 analysis.csv"
index_GPIO1 = 52
index_GPIO2 = 60
index_GPIO3 = 68
index_GPIO4 = 76
index_GPIO5 = 84
reg_GPIO = r"A: ([\d\.]+)V  /  B: ([\d\.]+)V  /  C: ([\d\.]+)V  /  D: ([\d\.]+)V"
index_panic = 108
reg_panic = r"Panic 1 Low: (PASS|FAIL) \(([\d\.]+)\) / High: (PASS|FAIL) \(([\d\.]+)\)    Panic 2 Low: (PASS|FAIL) \(([\d\.]+)\) / High: (PASS|FAIL) \(([\d\.]+)\)"
index_12V = 124
reg_12V = r"Int(ernal)?: ([\d\.]+)V / V(B|b)att A: ([\d\.]+)V"
index_5V = 116
reg_5V = r"([\d\.]+)"

with open(input_filename) as f:
    with open(output_filename, 'w') as out_file:
        reader = csv.reader(f)
        headers = reader.next()
        for items in reader:
            out_array = []
            # GPIO1
            m = re.search(reg_GPIO, items[index_GPIO1])
            if not m:
                print "No match for GPIO1"
                out_array += ['']*4
            else:
                out_array += [m.group(1), m.group(2), m.group(3), m.group(4)]
            # GPIO2
            m = re.search(reg_GPIO, items[index_GPIO2])
            if not m:
                print "No match for GPIO2"
                out_array += ['']*4
            else:
                out_array += [m.group(1), m.group(2), m.group(3), m.group(4)]
            # GPIO3
            m = re.search(reg_GPIO, items[index_GPIO3])
            if not m:
                print "No match for GPIO3"
                out_array += ['']*4
            else:
                out_array += [m.group(1), m.group(2), m.group(3), m.group(4)]
            # GPIO4
            m = re.search(reg_GPIO, items[index_GPIO4])
            if not m:
                print "No match for GPIO4"
                out_array += ['']*4
            else:
                out_array += [m.group(1), m.group(2), m.group(3), m.group(4)]
            # GPIO5
            m = re.search(reg_GPIO, items[index_GPIO5])
            if not m:
                print "No match for GPIO5"
                out_array += ['']*4
            else:
                out_array += [m.group(1), m.group(2), m.group(3), m.group(4)]
            # Panic Lines
            m = re.search(reg_panic, items[index_panic])
            if not m:
                print "No match for Panic Lines: {}".format(items[index_panic])
                out_array += ['']*4
            else:
                out_array += [m.group(2), m.group(4), m.group(6), m.group(8)]
            # 5V
            m = re.search(reg_5V, items[index_5V])
            if not m:
                print "No match for 5V: {}".format(items[index_5V])
                out_array += ['']
            else:
                out_array += [m.group(1)]
            # 12V
            m = re.search(reg_12V, items[index_12V])
            if not m:
                print "No match for 12V: {}".format(items[index_12V])
                out_array += ['', '']
            else:
                out_array += [m.group(2), m.group(4)]

            out_file.write(DELIMITER.join(out_array) + '\n')
