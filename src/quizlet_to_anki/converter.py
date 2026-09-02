"""converter.py — THE WRITER.

Job: take a list of Card objects (the contract from models.py) and write a real
.apkg file to disk. This half knows about Anki and genanki. It knows NOTHING about
Quizlet — it never imports the scraper, and it doesn't care where the cards came from.

This is the half you build SECOND, because you can test it with fake cards and no
internet. Once a real .apkg imports into Anki, this file is done. See EXPLANATION.md
§4 and §8.

--------------------------------------------------------------------------------
YOUR JOB:

Write a function, roughly:

    def build_deck(cards: list[Card], deck_name: str, output_path: str) -> None:
        ...

that turns `cards` into a genanki deck and writes it to `output_path`.

The genanki recipe (see the four objects in our chat — Model, Note, Deck, Package):

  1. Define a genanki.Model:
       - Give it a unique MODEL_ID (see the WARNING below).
       - Give it fields: [{"name": "Front"}, {"name": "Back"}].
       - Give it a template that shows Front on the question side and Back on the
         answer side. (genanki's README has a copy-pasteable basic template.)
  2. Make a genanki.Deck(DECK_ID, deck_name).
  3. For each Card in `cards`:
       - make a genanki.Note(model=<your model>, fields=[card.term, card.definition])
       - deck.add_note(note)
  4. genanki.Package(deck).write_to_file(output_path)

  ⚠ WARNING — the ID gotcha from our chat:
     MODEL_ID and DECK_ID must be random integers that you pick ONCE and then
     HARD-CODE as constants at the top of this file. Do NOT generate a fresh random
     number on every run, or Anki will treat each import as a brand-new model/deck
     and you'll get duplicates. Generate them once with:
         import random; random.randrange(1 << 30, 1 << 31)
     then paste the two numbers in as constants and never change them.

TESTING THIS HALF (do this before touching the scraper):
  Feed it 2-3 hardcoded Cards, write out test.apkg, and import it into Anki by hand.
  If the cards show up correctly, the converter is PROVEN. That's the whole point of
  building this half first.
--------------------------------------------------------------------------------
"""

# from .models import Card   # you'll need this once you start writing build_deck

# TODO: import genanki, define MODEL_ID / DECK_ID constants, and write build_deck().
