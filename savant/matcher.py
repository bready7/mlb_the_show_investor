import json
import os
from difflib import get_close_matches
from pathlib import Path

CACHE_PATH = Path("savant/player_match_cache.json")
ITEM_DETAILS_PATH = Path("data/item_details.json")  # Adjust path as needed


def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


def load_item_details():
    if ITEM_DETAILS_PATH.exists():
        with open(ITEM_DETAILS_PATH, "r") as f:
            items = json.load(f)
            return items
    raise FileNotFoundError("item_details.json not found.")


def get_card_player_names():
    """
    Returns a list of player names from item_details.json
    """
    items = load_item_details()
    names = []

    for item in items:
        name = item.get("name")
        if name:
            names.append(name)
    
    return names


def match_player(real_name, card_names):
    """
    Fuzzy match a real player name to an MLB The Show card name.
    """
    matches = get_close_matches(real_name, card_names, n=1, cutoff=0.7)
    return matches[0] if matches else None


def get_matched_players(real_player_names):
    """
    Maps a list of real-world player names to closest MLB The Show card names.
    """
    cache = load_cache()
    card_names = get_card_player_names()

    matched = {}
    updated = False

    for name in real_player_names:
        if name in cache:
            matched[name] = cache[name]
        else:
            best_match = match_player(name, card_names)
            cache[name] = best_match
            matched[name] = best_match
            updated = True

    if updated:
        save_cache(cache)

    return matched
