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
