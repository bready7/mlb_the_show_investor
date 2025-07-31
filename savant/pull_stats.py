import csv
import time
import requests
from .matcher import get_matched_players
from utils.cache import save_csv

SAVANT_URL = "https://baseballsavant.mlb.com/statcast_search/csv"
OUTPUT_CSV = "data/players_stats.csv"

# These are the statcast columns we'll extract
SAVANT_FIELDS = [
    "player_name", "year", "team", "PA", "AVG", "OBP", "SLG", "wOBA",
    "xBA", "xSLG", "xwOBA", "Barrel%", "HardHit%", "K%", "BB%", "Sprint Speed (ft / sec)"
]

def pull_statcast_data(matched_players):
    stats = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for player in matched_players:
        try:
            params = {
                "hfPT": "", "hfAB": "", "hfGT": "", "hfC": "", "hfSea": "2024",
                "hfSit": "", "player_type": "batter",
                "hfOuts": "", "opponent": "", "pitcher_throws": "", "batter_stands": "",
                "hfInfield": "", "hfOutfield": "", "stadium": "",
                "hfFlag": "", "hfPull": "", "metric_1": "", "metric_2": "",
                "min_pas": "1", "type": "batter", "player_lookup": player["name"]
            }

            response = requests.get(SAVANT_URL, params=params, headers=headers)
            if response.status_code != 200:
                print(f"Failed to get data for {player['name']}")
                continue

            decoded = response.content.decode("utf-8")
            reader = csv.DictReader(decoded.splitlines())
            for row in reader:
                row_data = {k: row.get(k, "") for k in SAVANT_FIELDS}
                row_data["card_name"] = player["card_name"]
                row_data["uuid"] = player["uuid"]
                stats.append(row_data)
                break  # Only take the top result

            time.sleep(1.5)  # avoid hitting rate limits

        except Exception as e:
            print(f"Error pulling data for {player['name']}: {e}")

    return stats


if __name__ == "__main__":
    matched_players = get_matched_players()
    savant_stats = pull_statcast_data(matched_players)
    save_csv(OUTPUT_CSV, savant_stats, SAVANT_FIELDS + ["card_name", "uuid"])
    print(f"✅ Saved {len(savant_stats)} player stat rows to {OUTPUT_CSV}")

