"""
UDL Abuse Report
Author: Ryan Vilbrandt
Date: 2018-10-26

A script to pull all UDLs that were assigned to No Driver Reason, but are longer than 20 miles. Requested by Knight
so we can provide a report to them for disciplinary purposes.

This script is meant to be run standalone, so does not have access to any of the rest of the zapy infrastructure or
config files. It was put in this repo for lack of a better home. If you have a better place for it to live, please feel
free to move it.
"""

from configparser import RawConfigParser
from time import localtime, strftime
import csv
import traceback

import psycopg2

#### EDIT THESE ####
ACCOUNT = "dbr47_rep1023"
MAX_MILES = 20
CSV_OUTPUT = "outputs/udl_report.csv"
####################

MILES_TO_METERS = 1609.344
MAX_METERS = int(MAX_MILES * MILES_TO_METERS)

config = RawConfigParser()
config.read("inputs/zonar_credentials.ini")

HOST = config.get("Postgres", "host")
PORT = config.get("Postgres", "port")
POSTGRES_USER = config.get("Postgres", "user")
POSTGRES_PASSWORD = config.get("Postgres", "password")


def fetchall_to_dict(cursor):
    output_list = []
    for row in cursor.fetchall():
        output_list.append(
            dict(
                [(column[0], row[i]) for i, column in enumerate(cursor.description)]
            )
        )
    return output_list


##### DB CALLS BELOW ######

# Open DB connection
conn_string = "dbname='{}' host='{}' user='{}' password='{}' port='{}'".format(
    ACCOUNT, HOST, POSTGRES_USER, POSTGRES_PASSWORD, PORT
)
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

bad_udls = []
ud_reasons_table = []

# Start transaction
try:
    # Get UDLs with Non-Driver assignment and distance > MAX_MILES
    sql = """
SELECT * 
FROM hos.unknown_driving ud
JOIN users u
ON ud.assigned_by_dispatcher_id = u.id
WHERE (end_odometer - start_odometer) > {max_meters}
AND assignee_person_type=2;
""".format(max_meters=MAX_METERS)

    cur.execute(sql)
    bad_udls = fetchall_to_dict(cur)

    cur.execute("SELECT * FROM hos.unassigned_driver_reason;")
    ud_reasons_table = cur.fetchall()
except Exception as e:
    print(traceback.format_exc())
finally:
    conn.rollback()
    cur.close()

if bad_udls:
    headers = ["unknown_driving_id", "asset_id", "start_datetime", "end_datetime", "assignment_status_ts",
               "assignee_person_type", "assignee_person_id", "start_odometer", "end_odometer",
               "distance", "assigned_by_dispatcher_id", "name", "fname", "lname", "email", "active"]
    ud_reasons = dict([(row[0], row[1]) for row in ud_reasons_table])

    with open(CSV_OUTPUT, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        for i, row in enumerate(bad_udls):
            # Create datetime columns
            fmt = "%Y-%m-%d %H:%M:%S%z"
            row["start_datetime"] = strftime(fmt, localtime(int(row["start_epoch"])))
            row["end_datetime"] = strftime(fmt, localtime(int(row["end_epoch"])))
            # Update UD Reason
            assignee_person_id = row["assignee_person_id"]
            row["assignee_person_id"] = ud_reasons.get(assignee_person_id, assignee_person_id)
            # Calculate distance traveled
            try:
                row["distance"] = "{:.02f}".format(
                    (int(row["end_odometer"]) - int(row["start_odometer"])) / MILES_TO_METERS
                )
            except ValueError:
                row["distance"] = None
            # Write row
            writer.writerow([row[h] for h in headers])
