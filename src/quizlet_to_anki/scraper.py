"""scraper.py — THE READER.

Job: get the terms and definitions out of a Quizlet set and return them as a
list of Card objects (the contract from models.py). This half knows about Quizlet
and HTML. It knows NOTHING about Anki or genanki — its output is just Cards.

This is the half you build LAST, because it's the changeable, fights-with-Quizlet
part. By the time you get here, the converter is already proven, so any bug is
guaranteed to live in THIS file. See EXPLANATION.md §4, §6, §8.

--------------------------------------------------------------------------------
YOUR JOB (in stages — don't try to do all of this at once):

STAGE 1 — MVP / semi-manual (build this first):
  Write a function that takes raw HTML you've already saved (you open the set in
  your own logged-in browser, save the page, and point the tool at the file), and
  parses the terms + definitions out of it:

      def parse_html(html: str) -> list[Card]:
          ...

  Steps: feed `html` to BeautifulSoup, find the elements that hold terms and the
  ones that hold definitions, and build one Card per pair. Figuring out WHICH
  elements those are (the parsing rules) is the real work — inspect a saved page in
  your browser's devtools to discover the pattern. This is YOUR engineering.

STAGE 2 — fetch it ourselves (later):
      def fetch_html(url: str) -> str:
  Use requests to download the page. Expect this to fight back (login wall, bot
  detection) — see EXPLANATION.md §6. That's the lesson, not a failure.

STAGE 3 — browser automation (the real scraper, later):
  Replace fetch_html with a Playwright version that drives a real browser, so JS
  rendering and bot detection stop blocking you. Same output type (a list of Cards),
  so the converter never notices the swap — that's the contract paying off.

Keep every stage returning `list[Card]`. That is the promise this file makes to
the rest of the program; never break it.
--------------------------------------------------------------------------------
"""

# from .models import Card   # your return type
# from bs4 import BeautifulSoup
# import requests

# TODO Stage 1: write parse_html(html: str) -> list[Card]
