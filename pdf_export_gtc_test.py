from configparser import RawConfigParser
from collections import OrderedDict

import requests

config = RawConfigParser()
config.read("inputs/zonar_credentials.ini")

# URL = "https://gtcdev.sea-001.zonarsystems.net/zlogs/log-export/get-pdf/"
# params = [
#     ("customer", "dbr47_rep1023"),
#     ("username", config.get("Zonar", "user")),
#     ("password", config.get("Zonar", "password")),
#     ("dvrids", "1251"),
#     ("sts", "2018-10-01"),
#     ("ets", "2018-10-18"),
#     ("issum", "f"),
#     ("isvio", "f"),
#     ("isbw", "f")
# ]

url = "https://gtcdev.sea-001.zonarsystems.net/zlogs/log-export/get-pdf/"
params = [
    ("customer", "dbr47_rep1023"),
    ("username", config.get("Zonar", "user")),
    ("password", config.get("Zonar", "password")),
    ("dvrids", "1251"),
    # ("sts", "2018-10-01"),
    # ("ets", "2018-10-18"),
    ("issum", "f"),
    ("isvio", "f"),
    ("isbw", "f")
]

print(url + "?" + "&".join("{}={}".format(k, v) for k, v in params))

r = requests.get(url, params, verify=False)
print(r)
print(r.url)
open('outputs/driver_1251.pdf', 'wb').write(r.content)