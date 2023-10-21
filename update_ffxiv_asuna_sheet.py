import os
from json import loads, dumps
from time import sleep
from typing import List

import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SHEET_ID = os.environ["FFXIV_ASUNA_SHEET_ID"]
GOOGLE_SHEETS_SERVICE_ACCOUNT = loads(os.environ["GOOGLE_SHEETS_SERVICE_ACCOUNT"])
WORLD = 74  # Coeurl
items_dict = None
ITEM_INDEX, TYPE_INDEX, PRICE_INDEX, ID_INDEX = None, None, None, None


def get_service():
    creds = Credentials.from_service_account_info(GOOGLE_SHEETS_SERVICE_ACCOUNT)
    return build('sheets', 'v4', credentials=creds).spreadsheets().values()


def get_sheet_data(service, sheet_name):
    global ITEM_INDEX, TYPE_INDEX, PRICE_INDEX, ID_INDEX
    print("Loading Google Sheet...")
    range = f"{sheet_name}!A1:Q"
    result = service.get(spreadsheetId=SHEET_ID, range=range).execute()
    header_row: List[str] = result["values"][0]
    ITEM_INDEX = header_row.index("Item")
    TYPE_INDEX = header_row.index("Type")
    PRICE_INDEX = header_row.index("Universalis")
    ID_INDEX = header_row.index("Item ID (hidden)")
    items = []
    for row in result["values"][1:]:
        items.append({
            "name": row[ITEM_INDEX] if len(row) >= ITEM_INDEX + 1 else "",
            "type": row[TYPE_INDEX] if len(row) >= TYPE_INDEX + 1 else "",
            "id": row[ID_INDEX] if len(row) >= ID_INDEX + 1 else ""
        })
    return items


def fill_missing_item_ids(items):
    for item in items:
        if not item["id"]:
            item_ids = get_item_ids()
            name = item["name"]
            if item["type"] == "Dye" and not name.endswith(" Dye"):
                name += " Dye"
            # print(name)
            item_id = item_ids.get(name)
            # print(item_id)
            if item_id is not None:
                item["id"] = item_id
    # print(items)
    return items


def get_item_ids():
    global items_dict
    if items_dict:
        return items_dict
    r = requests.get(
        "https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json")
    d = r.json()
    items_dict = {v["en"]: k for k, v in d.items()}
    # first_keys = list(items_dict.keys())[:10]
    # print({k: items_dict[k] for k in first_keys})
    return items_dict


def get_item_prices(csv_items):
    # print(csv_items)
    item_ids = "%2C".join([d["id"] for d in csv_items if d["id"]])
    # item_ids = "6141"
    url = f"https://universalis.app/api/{WORLD}/{item_ids}?listings=1&entries=1&noGst=1&hq=nq"
    print(url)
    response = None
    for _ in range(3):
        response = requests.get(url)
        if response.ok:
            break
        sleep(5)
    else:
        raise Exception(response.status_code, response.content)
    response_json = response.json()
    # print(dumps(response_json, indent=4))
    return {d["itemID"]: d for d in response_json["items"]}


def find_sale_prices(csv_items, universalis_dict):
    for item in csv_items:
        # print(item)
        if not item["id"]:
            item["price"] = ""
            continue
        item_id = int(item["id"])
        if item_id not in universalis_dict:
            item["price"] = ""
            continue
        sale_item = universalis_dict[item_id]
        # print(dumps(sale_item, indent=2))
        item["price"] = sale_item["minPriceNQ"]
    return csv_items


def write_new_prices(service, sheet_name, items):
    # Write prices
    c = chr(ord("A") + PRICE_INDEX)
    r = f"{sheet_name}!{c}2:{c}"
    body = {
        "majorDimension": "COLUMNS",
        "range": r,
        "values": [[str(item["price"]) for item in items]]
    }
    service.update(spreadsheetId=SHEET_ID, range=r,
                   valueInputOption="USER_ENTERED", body=body).execute()
    # Write IDs
    c = chr(ord("A") + ID_INDEX)
    r = f"{sheet_name}!{c}2:{c}"
    body = {
        "majorDimension": "COLUMNS",
        "range": r,
        "values": [[item["id"] for item in items]]
    }
    service.update(spreadsheetId=SHEET_ID, range=r,
                   valueInputOption="USER_ENTERED", body=body).execute()


def process_sheet(service, sheet_name):
    items = get_sheet_data(service, sheet_name)
    items = fill_missing_item_ids(items)
    items_dict = get_item_prices(items)
    items = find_sale_prices(items, items_dict)
    write_new_prices(service, sheet_name, items)


def main():
    service = get_service()
    process_sheet(service, "Apartment - Asuna's Rest")
    print(f"The sheet is viewable at https://docs.google.com/spreadsheets/d/{SHEET_ID}/")


if __name__ == "__main__":
    main()
