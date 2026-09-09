"""Turns a list of Cards (list[Card]) into an Anki .apkg file."""
from .models import Card

import genanki
import zlib # for generating STABLE ID's
from pathlib import Path

def generate_id_from_string(text: str) -> int:
    # Generates a stable integer within genanki's valid range (1 << 30 to 1 << 31)
    return (zlib.crc32(text.encode('utf-8')) % (1 << 30)) + (1 << 30)

QUIZLET_MODEL = genanki.Model(
    generate_id_from_string("Quizlet Model"),
    'Quizlet Model',
    fields=[
        {'name':'Front'},
        {'name':'Back'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Front}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ]
)

def build_deck(card_list: list[Card], deck_name, apkg_name=None, output_dir=None):
    if apkg_name is None:
        apkg_name = f"{deck_name}.apkg"
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[2] / "generated_apkgs"

    deck = genanki.Deck(generate_id_from_string(deck_name), deck_name)

    for card in card_list:
        note = genanki.Note(
            QUIZLET_MODEL,
            fields=[card.front, card.back]
        )

        deck.add_note(note) 

    output_path = Path(output_dir) / apkg_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck).write_to_file(str(output_path))

