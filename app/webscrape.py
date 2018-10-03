from bs4 import BeautifulSoup
import requests
from config import *


def scrape():
    exchange_data = [
        {
            'data': 'hello',
            'program': 'Software',
            'university': 'NUS'
        },
        {
            'data': 'hello',
            'program': 'Engineering',
            'university': 'NUT'
        },
    ]

    req = requests.get(SEARCH_URL)
    soup = BeautifulSoup(req.text, "html.parser")
    exchange_data = soup.find_all('div', class_="blurb")

    return exchange_data


if __name__ == "__main__":
    print(scrape())
