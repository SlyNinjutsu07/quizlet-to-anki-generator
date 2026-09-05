"""Tests for the converter."""
import sys
from pathlib import Path

# Windows' console defaults to cp1252, which can't encode emoji or CJK characters.
# Force UTF-8 so printing ✅/❌ and Chinese text doesn't crash.
sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

# Make the `quizlet_to_anki` package importable no matter where this file is run
# from, by putting the project's `src/` folder on Python's import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from quizlet_to_anki.models import Card
from quizlet_to_anki.converter import build_deck


def test_build_deck():
    deck_name = "chinese-food"

    cards = [
        Card(front="炒饭", back="fried rice"),
        Card(front="酸辣汤", back="hot and sour soup"),
        Card(front="猪肉饺子", back="pork dumplings"),
    ]

    build_deck(cards, deck_name)

    # build_deck writes to <project>/generated_apkgs/<deck_name>.apkg by default,
    # so we look for exactly that file to confirm it worked.
    expected = Path(__file__).resolve().parents[1] / "generated_apkgs" / f"{deck_name}.apkg"

    if expected.exists():
        print(f"✅ Deck generated: {expected}")
    else:
        print(f"❌ Deck was NOT generated (expected it at {expected})")

    Path(f"{deck_name}.apkg").unlink(missing_ok=True)
    Path("generated_apkgs").rmdir()


if __name__ == "__main__":
    test_build_deck()
