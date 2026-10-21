"""Command-line entry point: runs the scraper, then the converter."""
import argparse
from . import scraper, converter
from tests import test_cli
import json
from pathlib import Path
import os

with open("../../tests/sample_next_data.json") as file:
    test_json_string = file.read()

def check_path_valid(path):
    if path.is_dir():
        ...

def run_generation(deck_name, url=None, output_dir=None):
    '''The main function that runs scraper.py and converter.py in-sync'''
    output_dir = output_dir or "./generated_apkgs"
    next_data_dict = scraper.fetch_next_data(url) | json.loads(test_json_string)
    study_items = scraper.find_redux_to_json(next_data=next_data_dict)
    card_list = scraper.extract_cards(studiable_items=study_items)
    converter.build_deck(card_list=card_list, deck_name=deck_name, output_dir=output_dir)
    return output_dir

def main() -> None:
    parser = argparse.ArgumentParser(prog="qta")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("test-wiring", help="tests scraper + converter capability and returns True if an apkg was generated from sample data")

    args = parser.parse_args()

    # path_to_gen = input | "./generated_apkgs"

    # if args.command == 'test-wiring':
    #     run_generation(None, "sample", "./generated_apkgs")
    #     isGen = False
    #     if Path("./generated_apkgs/sample.apkg").exists():
    #         print(f'Sample apkg was generated at quizlet-to-anki-generation/generated_apkgs')
    #         isGen = True
    #     else:
    #         print(f'Failed to generate')

    #     if isGen:
    #         Path("./generated_apkgs/sample.apkg").unlink()
    #         print("File generated, and removed successfully")

    if args.command == "convert":
        ...




if __name__ == "__main__":
    main()
