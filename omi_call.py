from ConfigParser import RawConfigParser

import requests

OMI_URL = "https://hosdemo.zonarsystems.com/interface.php"
ACCOUNT = "devswi0001"

config = RawConfigParser()
config.read("inputs/zonar_credentials.ini")

USERNAME = config.get("Zonar", "OMI username")
PASSWORD = config.get("Zonar", "OMI password")

params = {
    "customer": ACCOUNT,
    "username": USERNAME,
    "password": PASSWORD,
    "action": "adminoperators", 
    "operation": "add", 
    "format": "xml", 
    "fname": "Ryan1",
    "lname": "Vilbrandt", 
    "location": "Home", 
    "tag": "2626",
    "pin": "2626",
    "cdl": "IHAVEACDLYAY",
    "logvers": "2"
}

response = requests.get(OMI_URL, params)

print(response)
print(response.url)
print(response.content)