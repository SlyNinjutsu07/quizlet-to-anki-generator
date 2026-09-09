"""Reads a Quizlet set and generates a list of Cards."""

from models import Card

import json
import requests
import sys
from bs4 import BeautifulSoup

# return list[Card]
def extract_cards(next_data: dict) -> None:

    pass

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


