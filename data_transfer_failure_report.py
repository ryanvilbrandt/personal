import csv
import re
from collections import defaultdict
from glob import glob


def dict_readers(wildcard_path):
    for path in glob(wildcard_path):
        print(path)
        with open(path, "rb") as f:
            for row in reversed(list(csv.DictReader(f))):
                yield row


def make_dd():
    return defaultdict(list)


error_dicts = defaultdict(make_dd)
for i, row in enumerate(dict_readers("inputs/extract-2020-07-07_14-07-18.csv")):
    date = row["date"]
    message = row["message"]
    m = re.search(r"finalizing datatransfer request (.*?), failure_trace=(.*)", message)
    if m:
        req_id = m.group(1)
        error_info = m.group(2)
        error_dicts[req_id]["error_list"].append(error_info)
    else:
        m = re.search(r"saving_request_status: account=(.*?), req_id=(.*?),", message)
        if m:
            req_id = m.group(2)
            account = m.group(1)
            error_dicts[req_id]["account"] = account
        else:
            print(message)
            print("")

print("Errors processed: {}".format(i + 1))
print("Unprocessed logs: {}".format(i - len(error_dicts) + 1))


# print("\nAttempt count: number of datatransfers that were attempted that many times")
# retries = defaultdict(int)
# for k, d in error_dicts.items():
#     error_list = d["error_list"]
#     if error_list:
#         retries[len(error_list)] += 1
# for k, v in sorted(retries.items(), key=lambda x: x[0]):
#     print("{}: {}".format(k, v))


# print("\nAverage number of attempts per unique datatransfer request, per account")
# retries_by_account = defaultdict(list)
# for k, d in error_dicts.items():
#     error_list = d["error_list"]
#     if error_list:
#         retries_by_account[d["account"]].append(len(error_list))
# for k, v in sorted(retries_by_account.items(), key=lambda x: x[0]):
#     print("{}: {}".format(k, sum(v)/float(len(v))))


# print("\nError rate by account")
# error_rate_by_account = defaultdict(list)
# for k, d in error_dicts.items():
#     if "account" in d:
#         error_list = d["error_list"]
#         error_rate_by_account[d["account"]] += error_list
# for k, v in sorted(error_rate_by_account.items(), key=lambda x: x[0]):
#     if v:
#         num_errors = len([x for x in v if x != "null"])
#         num_total = len(v)
#         print("{}: {} / {} ({:.2%})".format(k, num_errors, num_total, num_errors / float(num_total)))


print("\nError count by errors")
errors_by_type = defaultdict(int)
error_substrings = [
    ("ValueError: CDL not set for driver", "ValueError: CDL not set for driver"),
    ("NoEventsInDriverLogsException", "NoEventsInDriverLogsException: No events in logs for driver_id=*"),
    ("InvalidDriverIdException", "InvalidDriverIdException: DriverID=* does not exist"),
    ("in User List", "NoDriveEventsInUserLogsException: Cannot find * in User List"),
    ("FailureReasonEnum.PRECHECK", "FailureReasonEnum.PRECHECK"),
    ("HTTP Error 504: Gateway Time-out", "HTTP Error 504: Gateway Time-out"),
    ("Temporary failure in name resolution", "Temporary failure in name resolution"),
    ("Connection reset by peer", "Connection reset by peer"),
    ("Could not locate column in row for column 'get'", "Could not locate column in row for column 'get'")
]
for k, d in error_dicts.items():
    error_list = d["error_list"]
    for error in error_list:
        for es_match, es_print in error_substrings:
            if es_match in error:
                errors_by_type[es_print] += 1
                break
        else:
            if "Max retries exceeded with URL" in error:
                error = error[:error.find(" (Caused by NewConnectionError")]
                errors_by_type[error] += 1
            else:
                errors_by_type[error] += 1
for k, v in sorted(errors_by_type.items(), key=lambda x: x[1], reverse=True):
    print("{}: {}".format(k, v))

# print("")
# http_errors = defaultdict(list)
# for k, v in error_dicts.items():
#     if "HTTPError" in v.get("error", ""):
#         if "dg_mal_state" in v.get("raw", ""):
#             http_errors["dg_mal_state"].append(v["raw"])
#             # print(v["raw"])
#         else:
#             http_errors["other"].append(v)
# print("dg_mal_state: {}".format(len(http_errors["dg_mal_state"])))
# print("other: {}".format(len(http_errors["other"])))
# for item in sorted(http_errors["other"]):
#     print("")
#     print(item)
