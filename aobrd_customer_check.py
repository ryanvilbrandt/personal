import csv
import os
import re
from collections import defaultdict
from glob import glob


def dict_readers(wildcard_path, reverse_csv=False):
    for path in glob(wildcard_path):
        print(path)
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            if reverse_csv:
                reader = reversed(list(reader))
            for row in reader:
                yield row


customers = defaultdict(int)

for i, row in enumerate(dict_readers("inputs/1600367791_185471.csv")):
    m = re.search(r"- \[(.*?)] asset_query_kwargs=", row["_raw"])
    if m:
        # print(m)
        customers[m.group(1)] += 1


total_calls = sum(customers.values())
print("Total lines parsed: {}".format(total_calls))

subset_total = 0
for k, v in sorted(customers.items(), key=lambda x: x[1], reverse=True):
    # print(k, end=", ")
    subset_total += v
    print("{}: {}".format(k, v))

