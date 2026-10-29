# Daily Log

A daily log to keep track of the project over time and I don't have to manually look through the code to see what's been done.

I should've added this **WAY** before

## 9.26.26

Just analyzing what's been done:

- `converter.py` successfully generates a apkg for ANKI
    - tested successfully with `test_converter.py`
- `scraper.py` is still W.I.P:
    - ✅`find_redux_to_json`: successfully searches for the `dehydratedReduxStateKey` within the `__NEXT_DATA__` json and returns the `studiable_items` portion
    - ✅`extract_cards`: relies on the above, iterates through `studiable_items` and produces a list of `Card`s to later be used for `converter.py`
    - ❌ `scraper_main` is still **W.I.P** because we need to work with a **live URL**.

The only reason I've been able to validate the function of `find_redux_to_json` and `extract_cards` is because I have sample data to use in the `tests/` folder. However, **it's way too big** within the project (*reflects on Github*). So the priority is to establish `scraper_main` in order to go to a quizlet URL, get the html, find the `__NEXT_DATA__` and successfully return it for use. 


**TO-DO**: 
- (suggested by **CLAUDE**): add a test case to write a connection between `scraper.py` and `converter.py`. i.e. make sure that the collaboration actually produces a proper `.apkg` file from the sample test json.
- work with Playwright library to access Quizlet URL
- establish working test cases for all `scraper.py` functions
- ensure tests run well BEFORE reading data from a quizlet URL
- ensure that when quizlet URL is read, we print out an error within the terminal as to why the error occurred.

## 10.20.26
Too much time has been wasted, starting back on the consistent grind.

Current progress so far:
- established a working `run_generation` method
- installed pytest so I don't have to add a "test" command when using cli
- learned how to use `tmp_path` so I don't have to make my own and just build the deck into that
    - also stopped reading file with "./sample_next_data.json", because doing `Path(__file__).parent / ...` gets the parent of cli.py and then I can find the json file
- ✅ finished `test_wiring`, runs fine through pytest

**TO-DO**:
- more test cases to write for `scraper.py` and `converter.py`
- work with Playwright library to access Quizlet URL
- establish working test cases for all `scraper.py` functions
- ensure tests run well BEFORE reading data from a quizlet URL
- ensure that when quizlet URL is read, we print out an error within the terminal as to why the error occurred.

## 10.21.26
Made a few corrections to some code

- removed a unecessary `test_url` and `test_next_data_exists` because thats just runtime behavior we have to look out for
- modified `test_build_deck` to use `pytest` and `tmp_path` instead.

**TO-DO**:
- ✅ ~~more test cases to write for `scraper.py` and `converter.py`~~ cleaned up `test_cli.py` and `test_converter.py`
- work with Playwright library to access Quizlet URL
- ~~ensure tests run well BEFORE reading data from a quizlet URL~~ <- establish URL checking and NEXT_DATA existence during runtime through `scraper.py` exception handling.
    - ensure that when quizlet URL is read, we print out an error within the terminal as to why the error occurred.
- establish working test cases for all `scraper.py` functions

## 10.24.26
Currently having some ideas of later transitioning this project into a chrome extension too, rather than a CLI app. I think it'd be much easier for people to use if I distribute it.

Also removed BeautifulSoup and transitioned to using Playwright, which was the inital intention. The reasoning is that using BeautifulSoup would require me to use `requests` which is treated as an HTTP client, rather than a response being received from an actual browser, in order to get HTML code and find **"__NEXT_DATA__"**. So, because Quizlet uses Cloudflare, that method of scraping would automatically get rejected.

Using Playwright allows me to use an "instance" of a browser, so it can actually access the HTML code of the Quizlet URL (which in this case would be the URL that shows all the cards).

- modified `fetch_next_data` in `scraper.py` by removing BeautifulSoup functionality and replacing with Playwright
    - also added `TimeoutError` in the case that it CANT find the **'__NEXT_DATA__'**.
- added new arguments in `cli.py` for the url, naming, and setting the output directory
    - there's a thing called `"setTitle"`, in the **"__NEXT_DATA__"** - I need to get that and set that as the default

**TO-DO**:
- ✅ cleaned up `test_cli.py` and `test_converter.py`
- 🟨 work with Playwright library to access Quizlet URL
    - ✅ establish URL checking and NEXT_DATA existence during runtime through `scraper.py` exception handling.
    - add `"setTitle"` as default
    - ensure that when quizlet URL is read, we print out an error within the terminal as to why the error occurred.
- establish working test cases for all `scraper.py` functions

