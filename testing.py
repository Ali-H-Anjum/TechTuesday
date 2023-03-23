import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import random
import logging
import time
from googlesearch import search
import urllib

def google_scrape(url):
    thepage = urllib.urlopen(url)
    soup = BeautifulSoup(thepage, "html.parser")
    return soup.title.text

i = 1
query = 'search this'
for url in search(query, stop=10):
    a = google_scrape(url)
    print (str(i) + ". " + a)
    print (url)
    print (" ")
    i += 1

# Configure logger to handle errors
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.ERROR)

# Download NLTK punkt package
import nltk
nltk.download('punkt')

# Set up summarizer parameters
LANGUAGE = 'english'
SENTENCES_COUNT = 10
stemmer = Stemmer(LANGUAGE)
summarizer = LsaSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

# Set up search parameters
today = date.today()
last_monday = today - timedelta(days=today.weekday()) - timedelta(days=0)
page_num = 0
count = 0
max_results = 10
links = []

while count < max_results:
    searchUrl = f"https://www.bing.com/search?q=technology+news:{last_monday}+until:{today}&tbm=nws&start={page_num}"
    print(searchUrl, count)
    try:
        response = requests.get(searchUrl)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting search results from Google: {e}")
        print("Error getting search results from Google: {}".format(e))
        break
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for search_result in soup.select(".tF2Cxc"):
        url = search_result.find("a")["href"]
        if not url.startswith('http'):
            continue
        if 'support.google.com' in url:
            continue
        
        try:
            r = requests.get(url)
            time.sleep(1)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting article from {url}: {e}")
            continue
        
        if r.status_code in [403, 404]:
            continue
        
        links.append(url)
        count += 1
        
        if count >= max_results:
            print("bruh")
            break
    

if not links:
    print("No links found.")
    exit()

random_link = random.choice(links)

try:
    parser = HtmlParser.from_url(random_link, Tokenizer(LANGUAGE))
    summary = summarizer(parser.document, SENTENCES_COUNT)
    summary = summary[2:]
    
    print("Link: ", random_link)
    print("Summary: ")
    for sentence in summary:
        print(sentence)
        
except requests.exceptions.RequestException as e:
    logging.error(f"Error summarizing article from {random_link}: {e}")


