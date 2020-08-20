"""
    That module contains methods of searching and parsing music
"""
import re
import os
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


TOKEN = '9rt5dQe-trAD4-IyB-D0a8wwKCC6e9_zgecN-INNITdBuYpz6XxvoWSV6adGeNAA'
# os.environ["GENIUS_TOKEN"]
BASE_URL = "http://api.genius.com"
headers = {'Authorization': 'Bearer ' + TOKEN}
SEARCH_URL = BASE_URL + "/search"


def get_lyrics(url):
    """
        Function that parsing lyrics by url
    """
    lyrics = None
    while lyrics is None:
        try:
            session = HTMLSession()
            page = session.get(url)
            html = BeautifulSoup(page.content, 'html.parser')
            lyrics = html.findAll("div", {"class": "lyrics"})[0].get_text()
        except:
            pass

    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics

def get_urls(query):
    """
        Function that gets urls from search query
    """
    params = {'q': query}
    response = requests.get(SEARCH_URL, params=params, headers=headers).json()

    data = {}
    keyboard_data = {}
    k = 0
    for i in response['response']['hits']:
        name = i['result']['full_title'].replace(u'\xa0', ' ')
        keyboard_data[name] = k
        url = i['result']['url']
        image_url = i['result']['song_art_image_url']
        data[k] = {
            'url' : url,
            'image_url' : image_url
        }
        k += 1

    return data, keyboard_data
