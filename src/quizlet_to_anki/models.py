"""models.py — THE CONTRACT.

This file defines the single data structure that flows between the scraper and the
converter: what a "card" is. Both halves depend on this file and agree on this shape.
Nothing else in the project decides what a card looks like — only here.

See EXPLANATION.md §4 for why this boundary exists.

--------------------------------------------------------------------------------
YOUR JOB (start here — this is the first thing you write, ~10 minutes):

Define a `Card`. A card has exactly two pieces of text: a term and a definition.

TODO:
  1. Import `dataclass` from the `dataclasses` module.
  2. Define a class `Card` decorated with `@dataclass`, with two str fields:
         term: str
         definition: str
  3. (Optional, nice-to-have) make it frozen (@dataclass(frozen=True)) so a Card
     can't be accidentally mutated after creation. Ask yourself: why might
     immutability be a *good* default for a data-contract object?

Why a dataclass instead of a plain dict {"term": ..., "definition": ...}?
  - You get autocomplete and typo-safety: card.term (a typo like card.trem errors
    loudly) vs card["term"] (a typo returns a silent KeyError at runtime).
  - It's self-documenting: the class IS the spec of what a card contains.
  - The EXPLANATION used a dict to teach the idea; a dataclass is the grown-up form
    of the same idea.

When you're done, you should be able to open a Python shell and do:
    >>> from quizlet_to_anki.models import Card
    >>> c = Card(term="Bonjour", definition="Hello")
    >>> c.term
    'Bonjour'
--------------------------------------------------------------------------------
"""

# TODO: write the Card dataclass here.
