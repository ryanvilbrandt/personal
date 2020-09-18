import base64
import gzip
import os
from json import loads, dumps, load, dump


def remove_ds_without_violations(json):
    duty_statuses = json["data"]["duty_statuses"]
    duty_statuses_with_violations = []
    for ds in duty_statuses:
        if "violations" in ds:
            duty_statuses_with_violations.append(ds)
    json["data"]["duty_statuses"] = duty_statuses_with_violations


def get_file_size(filepath, original_size):
    size = os.stat(filepath).st_size
    return "{:,} bytes ({:.0%} compressed)".format(size, size / float(original_size))


def get_file_sizes(input_filepath):
    output_filepath = "outputs/temp.txt"
    base64_filepath = "outputs/temp_b64.txt"
    original_size = os.stat(input_filepath).st_size
    print("Raw file size: {}".format(get_file_size(input_filepath, original_size)))

    with open(input_filepath) as f:
        json = load(f)

    with gzip.open(output_filepath, 'wb') as f:
        dump(json, f)
    print("Raw file size (gzipped): {}".format(get_file_size(output_filepath, original_size)))

    with open(output_filepath, 'rb') as in_f:
        with open(base64_filepath, 'wb') as out_f:
            base64.encode(in_f, out_f)
    print("Raw file size (gzipped, base64): {}".format(get_file_size(base64_filepath, original_size)))

    remove_ds_without_violations(json)

    with open(output_filepath, 'w') as f:
        dump(json, f)
    print("Raw file size (filtered): {}".format(get_file_size(output_filepath, original_size)))

    with gzip.open(output_filepath, 'wb') as f:
        dump(json, f)
    print("Raw file size (filtered, gzipped): {}".format(get_file_size(output_filepath, original_size)))

    with open(output_filepath, 'rb') as in_f:
        with open(base64_filepath, 'wb') as out_f:
            base64.encode(in_f, out_f)
    print("Raw file size (filtered, gzipped, base64): {}".format(get_file_size(base64_filepath, original_size)))


get_file_sizes("inputs/re_firehose_1.txt")
print("")
get_file_sizes("inputs/re_firehose_2.txt")
print("")
get_file_sizes("inputs/re_firehose_3.txt")
print("")
get_file_sizes("inputs/re_firehose_4.txt")
print("")
