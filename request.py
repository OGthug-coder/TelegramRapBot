import requests
from bs4 import BeautifulSoup
import re
import os
from requests_html import HTMLSession


def get_lyrics(url):
    session = HTMLSession()
    page = session.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])         
    return lyrics

TOKEN = os.environ["GENIUS_TOKEN"]
base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer ' + TOKEN}
search_url = base_url + "/search"

def get_urls(query):
    params = {'q': query}
    response = requests.get(search_url, params=params, headers=headers).json()
    lyrics_url = response['response']['hits'][0]['result']['url']
    img_url = response['response']['hits'][0]['result']['song_art_image_url']
    return (lyrics_url, img_url)