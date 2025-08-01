import requests
import csv
import json
import os

DATA_DIR = "data"
BATTERS_FILE = os.path.join(DATA_DIR, "players_batters.json")
PITCHERS_FILE = os.path.join(DATA_DIR, "players_pitchers.json")

CSV_URLS = {
    "batters": "https://baseballsavant.mlb.com/statcast_search/csv?all=true&year=2025&type=batter",
    "pitchers": "https://baseballsavant.mlb.com/statcast_search/csv?all=true&year=2025&type=pitcher"
}

def fetch_player_data(url):
    print(f"Downloading CSV from {url}...")
    resp = requests.get(url)
    resp.raise_for_status()

    decoded = resp.content.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    # Collect all rows (each row is a dict of stats for a player event)
    # We'll extract unique player_name keys and save all data, or filter later
    players = {}
    for row in reader:
        name = row.get("player_name")
        if not name:
            continue
        # Store or update player info — here just collecting last row for simplicity
        players[name] = row
    print(f"Fetched data for {len(players)} players.")
    return players

def save_json(data, filename):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved data to {filename}")

def main():
    batters = fetch_player_data(CSV_URLS["batters"])
    save_json(batters, BATTERS_FILE)

    pitchers = fetch_player_data(CSV_URLS["pitchers"])
    save_json(pitchers, PITCHERS_FILE)

if __name__ == "__main__":
    main()
