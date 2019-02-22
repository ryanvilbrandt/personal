import sys
from json import dumps, loads
from urllib.parse import quote

from requests import post
from requests.auth import HTTPBasicAuth


def make_call(url, username, password, args):
    url += '?' + "&".join([f"{k}={v}" for k, v in args.items()])
    print(url)
    return post(url, auth=HTTPBasicAuth(username, password))


def quote_zargs(zargs):
    return quote(dumps(zargs)).replace('"', "%22")


url = 'https://gtc.zonarsystems.net/interface.php?action=twentytwenty&operation=common&app=hos&service=dgmaldatadump&customer=lak6855&zargs=%7B%22asset_id%22%3A%20%2292%22%2C%20%22driver_id%22%3A%20%2271%22%2C%20%22start_ts%22%3A%20%222017-12-07%2000%3A00%3A00%22%2C%20%22end_ts%22%3A%20%222018-04-30%2000%3A00%3A00%22%7D'
username = "zonar"
password = "shuri.line45"
args = {
    "action": "twentytwenty", 
    "operation": "common", 
    "app": "hos", 
    "service": "dgmaldatadump", 
    "customer": "lak6855", 
}
zargs = {
    "asset_id": "92",
    "driver_id": "71",
    "start_ts": "2017-12-07 00:00:00",
    "end_ts": "2018-04-30 00:00:00"
}
args["zargs"] = quote_zargs(zargs)
# args["zargs"] = '%7B%22asset_id%22%3A%20%2292%22%2C%20%22driver_id%22%3A%20%2271%22%2C%20%22start_ts%22%3A%20%222017-12-07%2000%3A00%3A00%22%2C%20%22end_ts%22%3A%20%222018-04-30%2000%3A00%3A00%22%7D'

response = make_call(url, username, password, args)
if response.text.startswith('<?xml'):
    print(response.text)
    sys.exit(0)
json_response = loads(response.text)
print(json_response.keys())

print(dumps(json_response['dg_mal_state'], indent=4))

dg_mals = json_response['dg_mals']
dg_mals_filtered = [dg_mal for dg_mal in dg_mals
                    if dg_mal['event'].startswith("MALFUNCTION") and dg_mal['mdcode'] == "ENGINE_SYNCH"]
print(len(dg_mals_filtered))
print(dumps(dg_mals_filtered, indent=4))

print(len([dg_mal for dg_mal in dg_mals_filtered if dg_mal['event'] == "MALFUNCTION_SET"]))
print(len([dg_mal for dg_mal in dg_mals_filtered if dg_mal['event'] == "MALFUNCTION_CLEAR"]))

