import re, csv

filename = "search-results-2014-03-27-mje0796.csv"
output_file = "attribute_calls.csv"

with open(filename) as f:
    reader = csv.reader(f)
    with open(output_file, 'wb') as o:
        writer = csv.writer(o)
        header = reader.next()
        writer.writerow(header)
        for line in reader:
            line[0] = "'"+line[0]
            line[1] = "'"+line[1]
            line[2] = "'"+line[2]
            writer.writerow(line)
