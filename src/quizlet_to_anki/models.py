"""The dataclass for what the card should be: Card."""
from dataclasses import dataclass

@dataclass
class Card:
    front: str
    back: str