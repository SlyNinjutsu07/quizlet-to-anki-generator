# EXPLANATION — Quizlet → Anki tool

**Written:** 2026-09-02
**For:** the developer (you) — a plain-language walkthrough of the concepts and design decisions before we write any code.

Read this top to bottom once. You don't need to memorize it — it's here so the words I use later ("converter", "the contract", "venv") actually mean something. Nothing here is code you have to write yet.

---

## 1. The big picture: what are we even building?

The goal: **take a Quizlet study set and turn it into a `.apkg` file that Anki can import.**

Anki is a flashcard app. A `.apkg` is Anki's file format for "a deck of cards you can import." So our program's job is a translation:

```
   Quizlet set  ────►  our program  ────►  a .apkg file  ────►  you import it into Anki
 (lives online)                          (lives on disk)
```

That's the whole tool. Everything else is detail about *how* we do the middle box.

---

## 2. The two halves: scraper and converter

Notice the middle box actually has two very different jobs inside it:

1. **Get the data OUT of Quizlet.** Quizlet has the terms and definitions; we need to read them into our program. The piece of code that does this is called the **scraper**.
2. **Put the data INTO an Anki file.** Once we have the terms and definitions in hand, we need to write them out in Anki's format. The piece of code that does this is called the **converter**.

```
  ┌──────────────┐        ┌───────────────┐
  │   SCRAPER    │        │   CONVERTER   │
  │              │        │               │
  │ Quizlet ───► │ cards  │ ───► .apkg    │
  │ read the set │══════► │ write the file│
  └──────────────┘  the   └───────────────┘
                  handoff
```

**Scraper** = "reader." Its whole world is Quizlet. It knows nothing about Anki.
**Converter** = "writer." Its whole world is Anki. It knows nothing about Quizlet.

In between them there's a **handoff**: the scraper produces a plain list of cards, and the converter takes that same plain list of cards. Neither one cares how the other works — they only agree on *the shape of the thing being passed between them*. That agreed-upon shape is what I keep calling **the contract** (more on that in §4).

---

## 3. "Upstream" and "downstream" (sorry about the river 😭)

You're right, it's not a river. It's an old programming metaphor and I should have explained it.

Picture a factory conveyor belt. Raw material goes in one end, finished product comes out the other. Work flows in **one direction** along the belt.

- **Upstream** = *earlier* on the belt — closer to where the raw material enters. The steps that happen *before* the step you're talking about.
- **Downstream** = *later* on the belt — closer to where the finished product exits. The steps that happen *after*.

In our tool the belt runs: **Quizlet → scraper → converter → .apkg file.**

So when I say "the scraper is **upstream** of the converter," I just mean the scraper runs first and feeds the converter. And "you can swap the scraper without touching anything **downstream**" means: change the reader, and the writer (which comes later on the belt) doesn't notice, because all it ever sees is the handoff in the middle.

That's the entire meaning. Upstream = before, downstream = after. No water involved.

---

## 4. Why THIS architecture? (the "contract" idea)

"Architecture" just means *how we split the program into pieces and how those pieces talk to each other.* Here's the decision and the reasoning.

### The naive way (what NOT to do)

A beginner often writes one big blob:

```
one giant function that:
  - opens Quizlet
  - digs the terms out of the page
  - AND builds the Anki database
  - AND zips it into a .apkg
  all tangled together
```

This *works* on day one and becomes a nightmare on day two. Why? Because Quizlet changes its website every few months. When it does, you have to go dig around inside code that's also full of Anki-file logic — and it's terrifyingly easy to break the Anki part while fixing the Quizlet part. The two concerns are glued together, so a change to one risks the other.

### The way we're doing it: split at the handoff

Instead, we define **one simple data structure in the middle** and make it a hard boundary. A single card is just:

```
a card = { "term": "Bonjour",  "definition": "Hello (French)" }
```

and the handoff is just **a list of those**:

```
[
  { "term": "Bonjour",  "definition": "Hello (French)" },
  { "term": "Merci",    "definition": "Thank you" },
  ...
]
```

That list is **the contract**. It's a promise between the two halves:

> "The scraper promises to *produce* a list of cards in this exact shape.
>  The converter promises to *accept* a list of cards in this exact shape.
>  Neither one is allowed to care about anything else the other does."

### Why this is worth it

Three concrete payoffs, and they're the reason senior engineers reach for this reflexively:

1. **Blast radius.** When Quizlet changes, the bug is *guaranteed* to be in the scraper. You never even open the converter file. The damage a change can do is contained ("small blast radius").
2. **You can build and test the halves independently.** You can test the converter *today* by feeding it a fake hardcoded list of 3 cards — no internet, no Quizlet needed. If a real `.apkg` pops out and imports into Anki, the converter is *done and proven*, forever. That's why our plan builds the converter first: it's the half you can fully nail down without fighting Quizlet.
3. **You can swap strategies.** Today the scraper might read a page you paste in. Next week it might drive a real browser. As long as it still coughs up that same list-of-cards, the converter never knows the difference. You've made the scary, changeable part *replaceable*.

This principle has a name you'll hear a lot: **separation of concerns.** Each piece has one concern, and only one. The scraper's concern is Quizlet. The converter's concern is Anki. The contract keeps them apart.

### How the folders reflect this

```
src/quizlet_to_anki/
├── models.py       # DEFINES the contract (what a "card" is)
├── scraper.py      # the READER  (Quizlet -> list of cards)
├── converter.py    # the WRITER  (list of cards -> .apkg)
└── cli.py          # the GLUE    (runs scraper, hands result to converter)
```

`models.py` is first on purpose — it's the contract, and both other files depend on it. `cli.py` ("command-line interface") is just the thin layer that wires them together and reads the options you type in the terminal. The structure *is* the architecture, made visible.

---

## 5. What the heck is a `.venv` folder?

`.venv` stands for **virtual environment**. To understand why it exists, you need one fact about Python:

When you `pip install` a library (like `genanki`), by default it gets installed **globally** — for your whole computer. That sounds convenient until you have two projects:

- Project A needs `genanki` version 0.13
- Project B needs `genanki` version 0.10

There's only one global slot, so installing one *breaks* the other. This is called **dependency hell**, and it's a genuine rite-of-passage headache.

A **virtual environment** solves it. It's a self-contained, private copy of Python-plus-its-libraries that lives **inside your project folder** (in the `.venv` folder). When it's "activated," any `pip install` you run drops the library into *that folder only*, not your whole machine.

Think of it as a **clean, sealed toolbox for this one project.** The tools you put in it are this project's tools. They don't spill into your other projects, and your other projects' tools don't spill into this one. Delete the `.venv` folder and it's like the project never touched your system — you can always rebuild it from `requirements.txt`.

### The mechanics you'll actually use

```bash
py -m venv .venv                     # create the toolbox (once, ever)
source .venv/Scripts/activate        # open/activate it (Git Bash on Windows)
# ...or in PowerShell:  .venv\Scripts\Activate.ps1
pip install genanki                  # now this goes INTO .venv, not globally
pip freeze > requirements.txt        # write down exactly what's installed
deactivate                           # close the toolbox when you're done
```

When it's active, your terminal prompt usually shows `(.venv)` at the front — that's how you know installs are landing in the toolbox and not on your whole system.

**`requirements.txt`** is the packing list for the toolbox: a plain text file listing every library and its version. Anyone (including future-you on a new laptop) can recreate the exact environment with `pip install -r requirements.txt`. This is why `.venv/` itself is *gitignored* — you never commit the heavy toolbox, you commit the lightweight packing list that lets anyone rebuild it.

---

## 6. How do scrapers actually work?

"Scraping" sounds mysterious. It's really just this: **a program pretends to be a web browser, asks a website for a page, and then digs the useful data out of what comes back.** Let's break that into the two steps.

### Step 1: Fetch — get the raw page

When *you* visit a Quizlet set, your browser sends an **HTTP request** to Quizlet's servers ("please give me the page at this URL"), and Quizlet sends back an **HTTP response** — mostly a big pile of **HTML** (the text-with-tags language that describes web pages). Your browser then *renders* that HTML into the pretty page you see.

A scraper does the exact same first part — send a request, get HTML back — just without the pretty rendering. In Python the classic tool for this is the `requests` library:

```
response = requests.get("https://quizlet.com/some-set")
html = response.text          # the raw HTML, as a giant string
```

### Step 2: Parse — dig the data out of the raw page

Now you have a giant string of HTML. Somewhere in that haystack are your terms and definitions. **Parsing** is the act of navigating that structure to pull out the specific bits you want. The classic tool is `BeautifulSoup`, which turns the HTML string into something you can search:

```
soup = BeautifulSoup(html)
terms = soup.find_all(... the pattern that marks a term ...)
```

That's scraping in its simplest form: **fetch, then parse.**

### Why Quizlet specifically is hard (and what that teaches you)

Simple fetch-and-parse works great on old-fashioned websites where the HTML that arrives already contains the data. **Quizlet is not one of those.** Two obstacles:

**Obstacle A — the data isn't in the first response.** Modern sites like Quizlet send you a nearly-empty HTML shell plus a bunch of JavaScript. Then the JavaScript runs *in your browser* and fetches the actual card data separately, filling it in afterward. So if you just `requests.get()` the page, the terms literally aren't there yet — you get the empty shell. `requests` can't run JavaScript; it only ever sees that first response.

**Obstacle B — bot detection.** Quizlet uses services (like Cloudflare) whose job is to notice "this visitor is a program, not a human" and block it. A bare `requests` call looks obviously robotic and often gets stopped at the door.

There are two honest ways around this, and they're the options from our plan:

- **Drive a *real* browser (Playwright / Selenium).** Instead of faking a request, you remote-control an actual browser. It runs the JavaScript (solves Obstacle A) and looks like a real human's browser (largely solves Obstacle B). Slower and heavier, but robust. This is the approach I recommend for the real version, and it's a genuinely employable skill.
- **Find the hidden data feed.** Since the JavaScript fetches the card data from *somewhere*, you can sometimes watch the browser's Network tab, find that exact request, and copy it. Clever and fast when it works — but brittle and easy to get blocked. A good "level 2" experiment, not a foundation.

Our MVP sidesteps *both* obstacles: you (a logged-in human, in your own browser) grab the page, and the tool just does the parsing. That proves the parsing + converter without fighting the fetch battle yet. We only take on the browser-automation fight once the rest of the tool is solid.

### The one-line mental model

> **Scraping = "fetch a page like a browser would, then parse the useful bits out of it."** The hard part on modern sites isn't the parsing — it's *fetching* data that a website actively tries to hide from programs.

---

## 7. Where each library fits

| Library      | Which half | Its one job |
|--------------|-----------|-------------|
| `genanki`    | converter | Build the `.apkg` (the Anki database + zip). Solved problem — we lean on it entirely. |
| `requests`   | scraper   | Send HTTP requests, get raw HTML back. (Used in the simple fetch approach.) |
| `BeautifulSoup` | scraper | Parse/search the HTML to pull out terms + definitions. |
| `playwright` | scraper   | Drive a real browser for pages that hide their data behind JavaScript + bot detection. (The recommended real scraper.) |

You will **not** write your own Anki-file logic or your own HTTP logic — those are solved. Your actual engineering is: **the parsing rules** (which patterns in Quizlet's page mark a term vs. a definition) and **the glue** that runs the pipeline. That's where your effort should go.

---

## 8. The build order, and why

1. **`models.py` — define the contract first.** Can't build a reader or writer until both sides agree on the shape being passed. ~10 minutes of work.
2. **`converter.py` — build the writer next.** Testable with fake data, zero internet. Once a real `.apkg` imports into Anki, this half is *done and proven*. Removes it as a variable forever.
3. **`scraper.py` — build the reader last.** The changeable, fight-with-Quizlet part. We tackle it knowing every remaining bug is in *this one file*, because §4's boundary guarantees it.
4. **`cli.py` — wire it together.** Read the URL/options from the terminal, run scraper → converter.

We de-risk from the certain (Anki format) toward the uncertain (Quizlet), so that when things get hard, the ground behind you is already solid.

---

*That's the conceptual map. When you've read it, tell me and we'll lay down the skeleton — then you start writing `models.py`.*
