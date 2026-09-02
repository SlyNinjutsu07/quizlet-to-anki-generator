"""cli.py — THE GLUE (command-line interface).

Job: the thin layer a human actually runs. It reads options from the terminal
(which set to convert, what to name the deck, where to write the .apkg), calls the
scraper to get Cards, hands those Cards to the converter, and reports the result.

It contains almost no logic of its own — it just wires the two halves together.
That's intentional: the interesting work lives in scraper.py and converter.py; cli.py
is the socket they plug into. See EXPLANATION.md §4.

--------------------------------------------------------------------------------
YOUR JOB (build this last, once scraper + converter both work):

  1. Use the `argparse` module to accept command-line arguments, e.g.:
         --input     path to a saved Quizlet HTML file (MVP), or a URL later
         --name      the deck name
         --output    where to write the .apkg (default: <name>.apkg)
  2. In a main() function:
         cards = <call the scraper to get list[Card]>
         build_deck(cards, deck_name=args.name, output_path=args.output)
         print how many cards were written and to where.
  3. The `if __name__ == "__main__": main()` line at the bottom lets you run this
     file directly with:  py -m quizlet_to_anki.cli --help

Think of main() as the ONLY place the two halves meet. If you ever find Quizlet
logic leaking into converter.py or Anki logic leaking into scraper.py, the fix is
usually "that coordination belongs here in the glue instead."
--------------------------------------------------------------------------------
"""

# import argparse
# from .scraper import parse_html      # (or fetch-based function later)
# from .converter import build_deck


def main() -> None:
    """Entry point. TODO: parse args, run scraper -> converter, report result."""
    raise NotImplementedError("TODO: wire the pipeline together")


if __name__ == "__main__":
    main()
