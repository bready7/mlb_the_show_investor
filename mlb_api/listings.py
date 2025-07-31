import requests
import json
from pathlib import Path
import os

API_URL = "https://mlb25.theshow.com/apis/listings.json"
CACHE_PATH = Path(os.path.join(os.getcwd(), "data/listings_raw.json"))

def fetch_live_series_cards(page=1):
    params = {
        "type": "mlb_card",
        "series_id": 1337,  # Live Series
        "page": page,
        "order": "desc",
        "sort": "rank"
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

def cache_listings(data):
    CACHE_PATH.parent.mkdir(exist_ok=True)
    print(f"Caching data to {CACHE_PATH} ...")
    print(f"Number of cards cached: {len(data.get('listings', []))}")
    with open(CACHE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_cached_listings():
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            return json.load(f)
    return None

def fetch_all_live_series_cards():
    all_listings = []
    page = 1

    while True:
        print(f"Fetching page {page}...")
        data = fetch_live_series_cards(page)
        listings = data.get("listings", [])
        all_listings.extend(listings)

        total_pages = data.get("total_pages", 1)
        if page >= total_pages:
            break
        page += 1

    return {
        "page": 1,
        "per_page": len(all_listings),
        "total_pages": 1,
        "listings": all_listings
    }

if __name__ == "__main__":
    data = fetch_all_live_series_cards()
    cache_listings(data)
    print(f"Fetched and cached a total of {len(data.get('listings', []))} cards.")
