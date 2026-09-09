"""Reads a Quizlet set and generates a list of Cards."""

from models import Card

import json
import requests
import sys
from bs4 import BeautifulSoup
from pathlib import Path

TARGET_KEY = 'studiableItems'

def find_redux_to_json(next_data: dict) -> list[dict]:
    if not next_data["props"]["pageProps"]["dehydratedReduxStateKey"]:
        raise ValueError("Could not find 'dehydratedReduxStateKey' string")

    # 1. reach the string
    redux_string = next_data["props"]["pageProps"]["dehydratedReduxStateKey"]

    # 2. parse redux string into a proper dict
    redux = json.loads(redux_string)

    # 3. iterable dict for study_items
    study_items = redux["studyModesCommon"]["studiableData"]["studiableItems"]
    return study_items


def extract_cards(studiable_items: list[dict]) -> list[Card]:
    cards = []
    for item in studiable_items:
        word_side, definition_side = item["cardSides"][0], item["cardSides"][1]
        front = word_side["media"][0]["plainText"]
        back = definition_side["media"][0]["plainText"]
        cards.append(Card(front=front, back=back))
    return cards

def extractor(url):
    # get url from user (handled by cli.py)
    url = "https://quizlet.com"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Decides whether the program gets to run or not
    try:
        response = requests.get(url)

        response.raise_for_status()
        # if above returns no error...
        print("Success! Parsing page...")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        sys.exit(1)

    # locate the __NEXT_DATA__ json
    soup = BeautifulSoup(response.text, "html.parser")
    next_data_tag = soup.find("script", id="__NEXT_DATA__")

    # check if the json data exists
    if next_data_tag and next_data_tag.string:
        next_data_json = json.loads(next_data_tag.string)

        try:
            set_data = next_data_json["props"]["pageProps"]["dehydratedState"]["queries"][0][
                "state"
            ]["data"]
            print(json.dumps(set_data, indent=2))
        except KeyError:
            print("The expected JSON path was not found in \'__NEXT_DATA__\'.")
    else:
        print("\'__NEXT_DATA__\' script tag not found on this page.")


data = json.loads(Path("tests/sample_next_data.json").read_text(encoding='utf-8'))
study_items = find_redux_to_json(data)
cards = extract_cards(study_items)
