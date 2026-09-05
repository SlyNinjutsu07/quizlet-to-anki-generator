"""Turns a list of Cards (list[Card]) into an Anki .apkg file."""
from models import Card

import genanki
import zlib # for generating STABLE ID's

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

 # TODO: add '-> bool'
def build_deck(cardList: list[Card], deckName):

    NEW_DECK = genanki.Deck(
        generate_id_from_string(deckName),
        deckName,
    )

    for card in cardList:
        NEW_CARD = genanki.Note(
            QUIZLET_MODEL,
            fields=[card.front, card.back]
        )
    pass
