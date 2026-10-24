"""Command-line entry point: runs the scraper, then the converter."""
import argparse
from . import scraper, converter
import json
from pathlib import Path
import os
import time
from playwright.sync_api import sync_playwright

def check_path_valid(path):
    if path.is_dir():
        ...

def run_generation(deck_name, url=None, output_dir=None):
    '''The main function that runs scraper.py and converter.py in-sync'''
    output_dir = output_dir or "./generated_apkgs"
    next_data_dict = scraper.fetch_next_data(url)  
    study_items = scraper.find_redux_to_json(next_data=next_data_dict)
    card_list = scraper.extract_cards(studiable_items=study_items)
    converter.build_deck(card_list=card_list, deck_name=deck_name, output_dir=output_dir)
    return output_dir

def main() -> None:
    parser = argparse.ArgumentParser(prog="qta")
    parser.add_argument("url", help="URL of the Quizlet set to convert")
    parser.add_argument("--name", help="sets the deck name (need quotes), otherwise default's the set's title")
    parser.add_argument("--output-dir", help="where to save the .apkg (default: ./generated_apkgs)")

    args = parser.parse_args()




if __name__ == "__main__":
    main()
