"""Reads a Quizlet set and generates a list of Cards."""

from .models import Card

import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeOut

# TARGET_KEY = 'studiableItems'

def find_redux_to_json(next_data: dict) -> list[dict]:
    """Find the ``dehydratedReduxStateKey`` and convert it into an iterable ``dict``,
    returning the ``studiableItems`` it contains."""

    if not next_data["props"]["pageProps"]["dehydratedReduxStateKey"]:
        raise ValueError("Could not find 'dehydratedReduxStateKey' string")

    # 1. reach the string
    redux_string = next_data["props"]["pageProps"]["dehydratedReduxStateKey"]

    # 2. parse redux string into a proper dict
    redux = json.loads(redux_string)

    # 3. iterable dict for study_items
    study_items = redux["studyModesCommon"]["studiableData"]["studiableItems"]
    return study_items

# relies on find_redux_to_json
def extract_cards(studiable_items: list[dict]) -> list[Card]:
    """Convert a list of ``studiableItems`` ``dicts`` into a list of ``Card`` objects,
    pairing each item's first two card sides as front and back."""
    cards = []
    for idx, item in enumerate(studiable_items):
        front, back = "", ""
        for side in item.get("cardSides", []): #find cards, else default to empty arr
            label = side.get("label")
            media = side.get("media") or []

            # check if media exists or if the text exists
            if not media or "plainText" not in media[0]:
                print(f"Warning: skipping malformed side (item {idx}, label={label!r})")
                continue

            text = media[0]["plainText"]
            if label == "word":
                front = text
            elif label == "definition":
                back = text

        if not front or not back:
            print(f"Warning: skipping item {idx} — missing front/back text")
            continue

        cards.append(Card(front=front, back=back))

    return cards


def fetch_next_data(url):
    """Fetch a Quizlet set page, locate its __NEXT_DATA__ JSON blob, and
    return the embedded set data."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        try:
            raw_next_data = page.locator('#__NEXT_DATA__').text_content(timeout=10000) # because the NEXT DATA is embedded as a constant string
        except PlaywrightTimeOut as e: 
            raise ValueError(f"No mention of \'__NEXT_DATA__\' at \'{url}\'")
        browser.close()

    if not raw_next_data:
        raise ValueError(f"No \'__NEXT_DATA__\' found at \'{url}\'")

    return json.loads(raw_next_data)
