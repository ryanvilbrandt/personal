import re, csv

DELIMITER = ','
input_filename = "sample cycle testing.csv"
output_filename = "sample cycle testing analysis.csv"
index_GPIO1 = 52
index_GPIO2 = 60
index_GPIO3 = 68
index_GPIO4 = 76
index_GPIO5 = 84
reg_GPIO = r"A: ([\d\.]+)V  /  B: ([\d\.]+)V  /  C: ([\d\.]+)V  /  D: ([\d\.]+)V"
index_12V = 116
reg_12V = r"Int(ernal)?: ([\d\.]+)V / V(B|b)att A: ([\d\.]+)V"
index_5V = 108
reg_5V = r"([\d\.]+)"
index_panic = 100
reg_panic = r"Panic 1 Low: PASS \(([\d\.]+)\) / High: PASS \(([\d\.]+)\)    Panic 2 Low: PASS \(([\d\.]+)\) / High: PASS \(([\d\.]+)\)"

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
                print "No match for Panic Lines"
                out_array += ['']*4
            else:
                out_array += [m.group(1), m.group(2), m.group(3), m.group(4)]
            # 5V
            m = re.search(reg_5V, items[index_5V])
            if not m:
                print "No match for 5V"
                out_array += ['']
            else:
                out_array += [m.group(1)]
            # 12V
            m = re.search(reg_12V, items[index_12V])
            if not m:
                print "No match for 12V"
                out_array += ['', '']
            else:
                out_array += [m.group(2), m.group(4)]

            out_file.write(DELIMITER.join(out_array) + '\n')
