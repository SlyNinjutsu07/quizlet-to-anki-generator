"""Reads a Quizlet set and generates a list of Cards."""

import requests
from bs4 import BeautifulSoup

# get url from user (handled by cli.py)
url = "https://quizlet.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    #do the scrape
    pass
else:
    print(f"Failed to load page. status code: {response.status_code}")