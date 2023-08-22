import os
from json import loads, dumps

import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SHEET_ID = os.environ["FFXIV_SEALS_SHEET_ID"]
GOOGLE_SHEETS_SERVICE_ACCOUNT = loads(os.environ["GOOGLE_SHEETS_SERVICE_ACCOUNT"])
WORLD = 74  # Coeurl


def get_service():
    creds = Credentials.from_service_account_info(GOOGLE_SHEETS_SERVICE_ACCOUNT)
    return build('sheets', 'v4', credentials=creds).spreadsheets().values()


def get_sheet_data(service, sheet_name):
    print("Loading Google Sheet...")
    range = f"{sheet_name}!A2:A"
    result = service.get(spreadsheetId=SHEET_ID, range=range).execute()
    items = []
    for row in result["values"]:
        if len(row) < 1:
            items.append({"ID": ""})
        else:
            items.append({"ID": row[0]})
    return items


def get_item_prices(csv_items):
    # print(csv_items)
    item_ids = "%2C".join([d["ID"] for d in csv_items if d["ID"]])
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


def find_sale_prices(csv_items, items_dict):
    sale_prices = []
    for item in csv_items:
        # print(item)
        if not item["ID"]:
            sale_prices.append("")
            continue
        item_id = int(item["ID"])
        if item_id not in items_dict:
            sale_prices.append("")
            continue
        sale_item = items_dict[item_id]
        # print(sale_item)
        recent_history = sale_item["recentHistory"]
        last_sale_price = recent_history[0]["pricePerUnit"] if recent_history else 0
        sale_prices.append(str(min(sale_item["minPriceNQ"], last_sale_price)))
    return sale_prices


def write_new_prices(service, sheet_name, sale_prices):
    body = {
        "majorDimension": "COLUMNS",
        "range": f"{sheet_name}!D2:D",
        "values": [sale_prices]
    }
    service.update(spreadsheetId=SHEET_ID, range=f"{sheet_name}!D2:D",
                   valueInputOption="USER_ENTERED", body=body).execute()


def process_sheet(service, sheet_name):
    items = get_sheet_data(service, sheet_name)
    items_dict = get_item_prices(items)
    sale_prices = find_sale_prices(items, items_dict)
    write_new_prices(service, sheet_name, sale_prices)


def main():
    service = get_service()
    process_sheet(service, "Company Seals")
    process_sheet(service, "Tomestones")
    print(f"The sheet is viewable at https://docs.google.com/spreadsheets/d/{SHEET_ID}/")


if __name__ == "__main__":
    main()
