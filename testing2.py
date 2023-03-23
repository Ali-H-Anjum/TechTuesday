from googlesearch import search
import urllib.request
from bs4 import BeautifulSoup
import requests

def google_scrape(url):
    thepage = urllib.request.urlopen(url)
    soup = BeautifulSoup(thepage, "html.parser")
    return soup.title.text

i = 1
query = 'technology news'
for url in search(query):
    response = requests.head(url, headers={'User-Agent': 'Mozilla/5.0'})
    status = response.raise_for_status()  # Raises an exception if status code is not 2xx
    r = requests.get(url)
    if status is None:
        a = google_scrape(url)
        print (str(i) + ". " + a)
        print (url)
        print (" ")
        i += 1