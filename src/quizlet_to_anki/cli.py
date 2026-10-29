"""Command-line entry point: runs the scraper, then the converter."""
import argparse
from pathlib import Path
from . import scraper, converter


def default_desktop() -> Path:
    home = Path.home()
    onedrive_desktop = home / "OneDrive" / "Desktop"
    if onedrive_desktop.exists():      # Windows with OneDrive backup (your case)
        return onedrive_desktop
    return home / "Desktop"            # macOS, Linux, non-OneDrive Windows

def check_path_valid(path):
    if path.is_dir():
        ...

def run_generation(deck_name, url=None, output_dir=None, isReverse=False):
    '''The main function that runs scraper.py and converter.py in-sync'''
    output_dir = output_dir or default_desktop()
    next_data_dict = scraper.fetch_next_data(url) 

    set_title = next_data_dict['props']['pageProps'].get('setTitle', 'Untitled')
    deck_name = deck_name or set_title

    study_items = scraper.find_redux_to_json(next_data=next_data_dict)
    card_list = scraper.extract_cards(studiable_items=study_items, isReverse=isReverse)
    converter.build_deck(card_list=card_list, deck_name=deck_name, output_dir=output_dir)
    return output_dir

def main() -> None:
    parser = argparse.ArgumentParser(prog="qta")
    parser.add_argument("url", help="URL of the Quizlet set to convert")
    parser.add_argument("--name", help="sets the deck name (need quotes), otherwise default's the set's title")
    parser.add_argument("--output-dir", help="where to save the .apkg (default: ./generated_apkgs)")
    parser.add_argument("--reverse", action="store_true", help="Flip the cards on either side -> front is the back, and back is the front")

    args = parser.parse_args()

    try:
        output = run_generation(deck_name=args.name, url=args.url, output_dir=args.output_dir, isReverse=args.reverse)
        print(f"Deck created at \'{output}\'")
    except Exception as e:
        print(f"ERR: {e}")
        raise SystemExit(1)



if __name__ == "__main__":
    main()
