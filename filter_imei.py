import csv

# filename = "Sienna QA Extracts.csv"
filename = "Sienna Test Result Log.csv"
d = {}

# Compile a dictionary of all SCIDs
# Each SCID has a list of three-tuples: IMEI, GPSID, Date
# This data can be used to find if any SCIDs were duplicated,
# using the IMEI as a unique identifier
with open(filename) as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        # indices for QA Extract file
        # scid = row[64].strip(' ')
        # imei = row[67].strip(' ')
        # date = row[1].strip(' ')
        # gpsid = row[2].strip(' ')
        # Indices for 4.6.7.1 Am Alive test result logs
        scid = row[204].strip(' ')
        imei = row[212].strip(' ')
        date = row[3].strip(' ')
        gpsid = row[44].strip(' ')
        scid_entries = d.get(scid, [])
        # Filter out the IMEIs for easy checking if the IMEIs
        # have already been added to the list
        imei_items = [item[0] for item in scid_entries]
        if not imei in imei_items:
            scid_entries.append([imei, gpsid, date])
            d[scid] = scid_entries
        # if i > 10:
        #     break

print "Number of SCIDs: {}".format(len(d))
print "\nSCIDs with duplicate entries:"

items = d.items()
items = sorted(items, key=lambda x: x[-1][-1][-1])
# print items

for k,v in items:
    if len(d[k]) > 1:
        print k,
        for item in d[k]:
            print "\t{}\t{}\t{}".format(*item)