"""The Card contract shared between scraper and converter."""
from dataclasses import dataclass

@dataclass
class Card:
    front: str
    back: str