import requests
import csv
import json
import os

OUTPUT_FILE = "savant/known_savant_players.json"
CSV_URLS = {
    "batters": "https://baseballsavant.mlb.com/statcast_search/csv?all=true&year=2025&type=batter",
    "pitchers": "https://baseballsavant.mlb.com/statcast_search/csv?all=true&year=2025&type=pitcher"
}

def fetch_player_names(url):
    print(f"Downloading CSV from {url}...")
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Failed to download CSV from {url}")
        return []

    decoded = resp.content.decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    player_names = set()
    for row in reader:
        name = row.get("player_name")
        if name:
            player_names.add(name)
    return player_names

def save_player_names(names):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(sorted(names), f, indent=2)
    print(f"Saved {len(names)} player names to {OUTPUT_FILE}")

if __name__ == "__main__":
    all_players = set()
    for player_type, url in CSV_URLS.items():
        players = fetch_player_names(url)
        all_players.update(players)

    save_player_names(all_players)
