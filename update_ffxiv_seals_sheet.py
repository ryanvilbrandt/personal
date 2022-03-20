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


def get_sheet_data(service):
    print("Loading Google Sheet...")
    range = "Company Seals!A2:A"
    result = service.get(spreadsheetId=SHEET_ID, range=range).execute()
    items = []
    for row in result["values"]:
        if len(row) < 1:
            items.append({"ID": ""})
        else:
            items.append({"ID": row[0]})
    return items


def get_item_prices(csv_items):
    item_ids = "%2C".join([d["ID"] for d in csv_items if d["ID"]])
    url = "https://universalis.app/api/74/{}?listings=1&entries=0&noGst=1&hq=nq".format(item_ids)
    print(url)
    response = requests.get(url)
    print(response)
    response_json = response.json()
    # print(dumps(response_json, indent=4))
    return {d["itemID"]: d for d in response_json["items"]}


def find_sale_prices(csv_items, items_dict):
    sale_prices = []
    for item in csv_items:
        print(item)
        if not item["ID"]:
            sale_prices.append("")
            continue
        item_id = int(item["ID"])
        if item_id not in items_dict:
            sale_prices.append("")
            continue
        sale_item = items_dict[item_id]
        print(sale_item)
        sale_prices.append(str(sale_item["minPriceNQ"]))
    return sale_prices


def write_new_prices(service, sale_prices):
    body = {
        "majorDimension": "COLUMNS",
        "range": "Company Seals!D2:D",
        "values": [sale_prices]
    }
    service.update(spreadsheetId=SHEET_ID, range="Company Seals!D2:D", valueInputOption="USER_ENTERED", body=body).execute()


def main():
    service = get_service()
    items = get_sheet_data(service)
    items_dict = get_item_prices(items)
    sale_prices = find_sale_prices(items, items_dict)
    write_new_prices(service, sale_prices)


if __name__ == "__main__":
    main()
