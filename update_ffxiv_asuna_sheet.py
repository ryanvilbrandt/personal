import os
from json import loads, dumps

import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SHEET_ID = os.environ["FFXIV_ASUNA_SHEET_ID"]
GOOGLE_SHEETS_SERVICE_ACCOUNT = loads(os.environ["GOOGLE_SHEETS_SERVICE_ACCOUNT"])
WORLD = 74  # Coeurl
items_dict = None


def get_service():
    creds = Credentials.from_service_account_info(GOOGLE_SHEETS_SERVICE_ACCOUNT)
    return build('sheets', 'v4', credentials=creds).spreadsheets().values()


def get_sheet_data(service, sheet_name):
    print("Loading Google Sheet...")
    range = f"{sheet_name}!A2:P"
    result = service.get(spreadsheetId=SHEET_ID, range=range).execute()
    items = []
    for row in result["values"]:
        items.append({
            "name": row[0] if len(row) >= 1 else "",
            "type": row[5] if len(row) >= 6 else "",
            "id": row[15] if len(row) >= 16 else ""
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
    response = requests.get(url)
    # print(response)
    # raise
    if not response.ok:
        raise Exception(response.content)
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
    body = {
        "majorDimension": "COLUMNS",
        "range": f"{sheet_name}!K2:K",
        "values": [[str(item["price"]) for item in items]]
    }
    service.update(spreadsheetId=SHEET_ID, range=f"{sheet_name}!K2:K",
                   valueInputOption="USER_ENTERED", body=body).execute()
    # Write IDs
    body = {
        "majorDimension": "COLUMNS",
        "range": f"{sheet_name}!P2:P",
        "values": [[item["id"] for item in items]]
    }
    service.update(spreadsheetId=SHEET_ID, range=f"{sheet_name}!P2:P",
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
