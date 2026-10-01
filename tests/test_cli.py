from src import quizlet_to_anki
from quizlet_to_anki import scraper, converter

import json
import os
from pathlib import Path


# PRECHECKS ->functions to check if a URL is valid first and can be read properly
def test_url(url):
    '''Checks if we can acquire a readable html from the url'''
    pass

def test_next_data_exists(): #return true or false
    '''Checks if __NEXT_DATA__ exists in the inner html'''
    pass

# TEST EITHER PY FILE
def test_scraper():
    pass

def test_converter():
    pass

# TEST BOTH ARE WIRED
def test_wiring():
    with open("./sample_next_data.json") as file:
        json_string = file.read()
        next_data = json.loads(json_string)

    studiable_items = scraper.find_redux_to_json(next_data)
    card_list = scraper.extract_cards(studiable_items)

    converter.build_deck(card_list, "Chinese Characters", "chinese-characters", "gen_apkg_wiring")
    file_path = Path("./gen_apkg_wiring/chinese-characters.apkg")

    res = file_path.is_file()

    if os.path.exists(file_path):
        os.remove(file_path)

    return res

def run_checks():
    # return all tests() (test1() and ... and testn())
    pass