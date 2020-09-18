from json import dumps, JSONDecodeError
from time import time

import requests
from pygments import highlight
from pygments.formatters.terminal256 import TerminalTrueColorFormatter
from pygments.lexers.data import JsonLexer
from pygments.lexers.html import HtmlLexer

# HOST = "http://zapy-hos.dev.zonarsystems.net"
# HOST = "http://qa-zapy-bip.sea-001.zonarsystems.net:8888"
# HOST = "http://zapy-hos.staging.zonarsystems.net"
# HOST = "http://qa-zapy-001.sea-001.zonarsystems.net:8888"
HOST = "http://zapy-bip.sea-001.zonarsystems.net:8888"
# HOST = "https://pyzhos.production.zonarsystems.net"

ENDPOINT = "/hos/version"
PARAMS = None

# ENDPOINT = "/ping"
# PARAMS = None

# ENDPOINT = "/hos/eldhossummary"
# PARAMS = {
#     "account": "dbr47_rep1023",
#     "driver_id": 1473,
#     "epoch": int(time())
# }

# ENDPOINT = "/hos/eld_data_transfer"
# PARAMS = {
#     "account": "mbl2020",
#     "driver_ids": 25,
#     "transmission_type": "web",
#     "start_day": "2020-08-29",
#     "end_day": "2020-09-01",
#     "email_addr": "ryan.v@zonarsystems.com"
# }

r = requests.post(HOST + ENDPOINT, params=PARAMS)

try:
    j = r.json()
    print(highlight(dumps(j, indent=2), JsonLexer(), TerminalTrueColorFormatter()))
    if not j["code"] == "success":
        print(j["data"]["trace"])
except JSONDecodeError:
    print(highlight(r.content, HtmlLexer(), TerminalTrueColorFormatter()))
