import requests
import datetime
import random
from bs4 import BeautifulSoup
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import concurrent.futures
import time
import nltk
import discord
nltk.download('punkt')

intents = discord.Intents.all()
intents.members = True  # Subscribe to the 'members' intent

client = discord.Client(intents=intents)

server_id = 1073326534628221050
channel_id = 1087802582497509517
today = datetime.date.today()
last_monday = today - datetime.timedelta(days=today.weekday()) - datetime.timedelta(days=0)


@client.event
async def on_ready():
    server = client.get_guild(server_id)
    channel = server.get_channel(channel_id) 
    await channel.send("Free me from my mortal toil")

@client.event
async def on_message(message):
    # Check if the message is in the #technology-news channel and starts with !tt 
    if message.channel.id == channel_id and "!tt" in message.content.lower():
        links = set()
        count = 0
        page_num = 0
        while count < 10:
            search_params = {
                "q": f"technology:{last_monday}+until:{today}",
                "tbm": "nws",
                "start": page_num
            }
            response = requests.get("https://www.google.com/search", params=search_params)
            await message.channel.send("Found {} usable links".format(len(links)))
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # use ThreadPoolExecutor to send multiple requests at once
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and href.startswith('/url?q='):
                        url = href[7:]
                        if not url.startswith('http'):
                            continue
                        if 'support.google.com' in url:
                            continue
                        futures.append(executor.submit(requests.get, url))
                for future in concurrent.futures.as_completed(futures):
                    try:
                        r = future.result()
                        if r.status_code == 200:
                            links.add(r.url)
                            count += 1
                            if count >= 10:
                                break
                    except requests.exceptions.RequestException as e:
                        print(e)
                        continue
                if count >= 10:
                    break
            
            page_num += 10
            
            # wait for a few seconds before checking the next page to avoid overwhelming the server
            time.sleep(1)

        random_link = random.choice(list(links))
        response = requests.get(random_link)
        LANGUAGE = 'english'
        SENTENCES_COUNT = 10
        parser = HtmlParser.from_url(random_link, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        summary = []
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
                summary.append(str(sentence))
        summary = summary[2:]
        await message.channel.send("Link: {}".format(random_link))
        await message.channel.send("Summary: ")
        for sentence in summary:
            await message.channel.send(sentence)
        

# Replace 'YOUR_BOT_TOKEN' with your own bot token
client.run('MTA4NzgzNDM0NjcwODI4MzQzMw.GyFkoX.MGFgB6TvXPAYj1vtVt9BaD2Dqrq2bUGqT46_fg')