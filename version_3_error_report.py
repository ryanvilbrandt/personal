import ast
import csv
import re
from collections import defaultdict
from glob import glob
from json import loads


def dict_readers(wildcard_path):
    for path in glob(wildcard_path):
        print(path)
        with open(path, "rb") as f:
            for row in reversed(list(csv.DictReader(f))):
                yield row


def make_dd():
    return defaultdict(list)


errors_list = []
for i, row in enumerate(dict_readers("inputs/extract-2020-06-01_09-06-39.csv")):
    m = re.search(r"params=(.*?), duration", row["message"])
    params = ast.literal_eval(m.group(1))
    # print(params)
    error_dict = {
        "account": params["args"][0],
        "driver_id": params["args"][1],
        "asset_id": params["args"][3]["asset_id"]
    }
    # print(error_dict)
    errors_list.append(error_dict)


print("\nError rate by account")
error_rate_by_account_asset_id = defaultdict(int)
for d in errors_list:
    # print(d)
    error_rate_by_account_asset_id[d["account"]] += 1
for k, v in sorted(error_rate_by_account_asset_id.items(), key=lambda x: x[0]):
    num_errors = v
    num_total = len(errors_list)
    print("{}: {} / {} ({:.2%})".format(k, num_errors, num_total, num_errors / float(num_total)))


print("\nError rate by account:asset_id")
error_rate_by_account_asset_id = defaultdict(int)
for d in errors_list:
    # print(d)
    error_rate_by_account_asset_id["{}:{}".format(d["account"], d["asset_id"])] += 1
for k, v in sorted(error_rate_by_account_asset_id.items(), key=lambda x: x[1], reverse=True):
    num_errors = v
    num_total = len(errors_list)
    print("{}: {} / {} ({:.2%})".format(k, num_errors, num_total, num_errors / float(num_total)))


asset_id_list = []
for k, v in sorted(error_rate_by_account_asset_id.items(), key=lambda x: x[1], reverse=True):
    account, asset_id = k.split(":")
    if account == "hoo3025":
        asset_id_list.append(asset_id)
# print(" OR ".join(["asset_id = {}".format(a) for a in asset_id_list]))
print(len(asset_id_list))
