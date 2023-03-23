from googlesearch import search
import urllib.request
from bs4 import BeautifulSoup
import requests
from googlesearch import search as search_v2
from datetime import date, timedelta

today = date.today()
last_monday = today - timedelta(days=today.weekday()) - timedelta(days=0)

def google_scrape(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        if soup.title is not None:
            return soup.title.text
        else:
            return None
    else:
        print(f"Error: {r.status_code}")
        return None

page_num = 0
query = 'https://www.bing.com/search?q=technology+news:{last_monday}+until:{today}&tbm=nws&start={page_num}'

results = search_v2(query)
print(results)
for url in results:
    title = google_scrape(url)
    if title is not None:
        print(title)
        print(url)
        print()
