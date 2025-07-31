# mlb_api/item_details.py
import requests
import json
from pathlib import Path
import os

API_URL = "https://mlb25.theshow.com/apis/item.json"
CACHE_DIR = Path(os.path.join(os.getcwd(), "data", "items_cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

LISTINGS_CACHE_PATH = Path(os.path.join(os.getcwd(), "data", "listings_raw.json"))

def fetch_item_details(uuid):
    params = {"uuid": uuid}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

def cache_item_details(uuid, data):
    cache_path = CACHE_DIR / f"{uuid}.json"
    with open(cache_path, "w") as f:
        json.dump(data, f, indent=2)

def load_cached_item(uuid):
    cache_path = CACHE_DIR / f"{uuid}.json"
    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)
    return None

def fetch_all_items_details():
    if not LISTINGS_CACHE_PATH.exists():
        print(f"Listings cache not found at {LISTINGS_CACHE_PATH}")
        return
    
    with open(LISTINGS_CACHE_PATH) as f:
        listings_data = json.load(f)
    
    listings = listings_data.get("listings", [])
    total = len(listings)
    print(f"Fetching details for {total} cards...")
    
    for idx, card in enumerate(listings, start=1):
        uuid = card.get("item", {}).get("uuid")
        if not uuid:
            print(f"[{idx}/{total}] No UUID found, skipping card")
            continue
        
        if load_cached_item(uuid):
            print(f"[{idx}/{total}] UUID {uuid} already cached, skipping.")
            continue
        
        print(f"[{idx}/{total}] Fetching details for UUID {uuid} ...")
        try:
            data = fetch_item_details(uuid)
            cache_item_details(uuid, data)
        except Exception as e:
            print(f"Error fetching {uuid}: {e}")

if __name__ == "__main__":
    fetch_all_items_details()
