from bs4 import BeautifulSoup
import requests
from config import *


def scrape():
    data = [
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

    return data