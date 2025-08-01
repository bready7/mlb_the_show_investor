import json
import os
from difflib import get_close_matches

KNOWN_SAVANT_PLAYERS_FILE = "savant/known_savant_players.json"
MATCHED_PLAYERS_FILE = "data/matched_players.json"

def load_known_savant_players():
    with open(KNOWN_SAVANT_PLAYERS_FILE, "r") as f:
        return json.load(f)

def save_matches(matches):
    with open(MATCHED_PLAYERS_FILE, "w") as f:
        json.dump(matches, f, indent=2)

def load_matches():
    if os.path.exists(MATCHED_PLAYERS_FILE):
        with open(MATCHED_PLAYERS_FILE, "r") as f:
            return json.load(f)
    return {}

def get_matched_players(card_names):
    """
    Takes in a list of card names from MLB The Show and matches them
    to Baseball Savant players using fuzzy name matching.
    """
    known_savant_players = load_known_savant_players()
    cached_matches = load_matches()

    updated = False
    for card_name in card_names:
        if card_name in cached_matches:
            continue

        # Try fuzzy matching
        match = get_close_matches(card_name, known_savant_players, n=1, cutoff=0.8)
        if match:
            cached_matches[card_name] = match[0]
        else:
            cached_matches[card_name] = None  # Unmatched for now
        updated = True

    if updated:
        save_matches(cached_matches)

    return cached_matches
