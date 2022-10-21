import json
from time import sleep

import requests
from colorama import Fore
from progressbar import *

WEBFLOW_COLLECTION_NAME = "Constituencies"
WEBFLOW_SITE_NAME = "getvoting-attempt-1"
WEBFLOW_TOKEN = "1073e4821feacac5dbd3fe141f32b649a4f7a4ad70157b22047ffe24f62f1dd6"
HEADERS = {
    'Accept-Version': "1.0.0",
    "Authorization": f"Bearer {WEBFLOW_TOKEN}",
}
BASE_API_URL = "https://api.webflow.com"

def get_collection_id(site_id: str, collection_name: str) -> str:
    r = requests.get(f"{BASE_API_URL}/sites/{site_id}/collections", headers=HEADERS)
    for collection in r.json():
        if collection['name'] == collection_name:
            r = requests.get(f"{BASE_API_URL}/collections/{collection['_id']}", headers=HEADERS)
            print(r.json())
            return collection['_id']

def get_collection_items(collection_id: str):
    r = requests.get(f"{BASE_API_URL}/collections/{collection_id}/items", headers=HEADERS)
    items = []
    while r.json().get('items'):
        items += r.json()['items']
        r = requests.get(f"{BASE_API_URL}/collections/{collection_id}/items?offset={len(items)}", headers=HEADERS)
    return {item['party-name']: item['_id'] for item in items}

def get_site_id(site_name: str) -> str:
    r = requests.get(f"{BASE_API_URL}/sites", headers=HEADERS)
    for site in r.json():
        if site['shortName'] == site_name:
            return site['_id']

def update_item(collection_id: str, item_id: str, key: str, value: dict):
    payload = json.dumps({'fields': {key: json.dumps(value)}})
    SPECIAL_HEADERS = {
        'Accept-Version': "1.0.0",
        "Authorization": f"Bearer {WEBFLOW_TOKEN}",
        'content-type': "application/json"
    }
    r = requests.patch(f"{BASE_API_URL}/collections/{collection_id}/items/{item_id}?live=true", data=payload, headers=SPECIAL_HEADERS)
    sleep(1.01)

def update_collection(items):
    site_id = get_site_id(WEBFLOW_SITE_NAME)
    collection_id = get_collection_id(site_id, WEBFLOW_COLLECTION_NAME)
    collection_items = get_collection_items(collection_id)
    
    widgets = [
        FormatLabel(Fore.GREEN + ""),
        " ",
        Percentage(),
        " ",
        Bar("/"),
        " ",
        RotatingMarker(),
    ]
    progressbar = ProgressBar(widgets=widgets, maxval=len(items))
    progressbar.start()
    for i, item in enumerate(items):
        code = item["Constituency code"]
        widgets[0] = FormatLabel(
            Fore.GREEN + f"Updating item for {code}... ({i+1}/{len(items)})"
        )
        progressbar.update(i)

        collection_item = collection_items.get(code)
        if collection_item:
            update_item(collection_id, collection_item, 'polldata', item)
    progressbar.finish()


