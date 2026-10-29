from quizlet_to_anki import scraper, converter

import json
from pathlib import Path
import pytest

# TEST BOTH ARE WIRED
def test_wiring(tmp_path):
    sample = Path(__file__).parent / "sample_next_data.json"
    next_data = json.loads(sample.read_text(encoding="utf-8"))

    studiable_items = scraper.find_redux_to_json(next_data)
    card_list = scraper.extract_cards(studiable_items, isReverse=False)

    converter.build_deck(card_list, "Chinese Characters", "chinese-characters", output_dir=tmp_path)
    assert (tmp_path / "chinese-characters.apkg").is_file()
