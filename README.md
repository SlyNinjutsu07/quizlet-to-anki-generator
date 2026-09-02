# quizlet-to-anki-generation

A command-line tool that turns a Quizlet study set into an Anki `.apkg` deck.

> **Status:** early development. Building the converter half first (proven, offline),
> then the scraper half. See [`EXPLANATION.md`](EXPLANATION.md) for the concepts and
> architecture behind the design.

## Architecture (one glance)

```
Quizlet ──► scraper.py ──►  list[Card]  ──► converter.py ──► .apkg ──► Anki
            (the reader)    (the contract)   (the writer)
```

Each half has one job and doesn't know about the other. The `Card` (in `models.py`)
is the only thing they share. Full reasoning in `EXPLANATION.md`.

```
src/quizlet_to_anki/
├── models.py       # the Card contract
├── scraper.py      # Quizlet  -> list[Card]   (the reader)
├── converter.py    # list[Card] -> .apkg      (the writer)
└── cli.py          # the glue (run this)
```

## Setup

```bash
py -m venv .venv                    # create the virtual environment (once)
source .venv/Scripts/activate       # activate it (Git Bash);  PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt     # install dependencies into the venv
```

## Usage

_Not wired up yet — coming once the pipeline is built._

```bash
py -m quizlet_to_anki.cli --help
```

## Note

Quizlet's Terms of Service prohibit automated scraping. This is a personal learning
project intended for use on your own study sets. Expect it to be brittle by nature.
