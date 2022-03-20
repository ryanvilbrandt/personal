import os
from json import loads

import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SHEET_ID = os.environ["FFXIV_SEALS_SHEET_ID"]
GOOGLE_SHEETS_SERVICE_ACCOUNT = loads(os.environ["GOOGLE_SHEETS_SERVICE_ACCOUNT"])


def get_service():
    creds = Credentials.from_service_account_info(GOOGLE_SHEETS_SERVICE_ACCOUNT)
    return build('sheets', 'v4', credentials=creds).spreadsheets().values()


def get_item_ids():
    r = requests.get("https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/apps/client/src/assets/data/items.json")
    item_dict = r.json()
    return {v["en"]: k for k, v in item_dict.items()}


def get_sheet_data(service, sheet_name):
    print("Loading Google Sheet...")
    range = f"{sheet_name}!B2:B"
    result = service.get(spreadsheetId=SHEET_ID, range=range).execute()
    items = []
    for row in result["values"]:
        if len(row) < 1:
            items.append({"Name": ""})
        else:
            items.append({"Name": row[0]})
    return items


def get_ids_for_items(csv_items, item_ids):
    for item in csv_items:
        if not item["Name"]:
            print("")
            # item["ID"] = ""
            continue
        if item["Name"] not in item_ids:
            raise ValueError(f"Couldn't find item '{item['Name']}'")
        print(item_ids[item["Name"]])
        # item["ID"] = item_ids[item["Name"]]
    return csv_items


def write_item_ids(service, sheet_name, items):
    body = {
        "majorDimension": "COLUMNS",
        "range": f"{sheet_name}!A2:A",
        "values": [str(item["ID"]) for item in items]
    }
    service.update(spreadsheetId=SHEET_ID, range=f"{sheet_name}!A2:A",
                   valueInputOption="USER_ENTERED", body=body).execute()


def process_sheet(service, item_ids, sheet_name):
    items = get_sheet_data(service, sheet_name)
    items = get_ids_for_items(items, item_ids)
    # write_item_ids(service, sheet_name, items)


def main():
    service = get_service()
    item_ids = get_item_ids()
    process_sheet(service, item_ids, "Tomestones")


if __name__ == "__main__":
    main()
