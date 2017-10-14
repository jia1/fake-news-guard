# Sources:
# Building a Chatbot using Telegram and Python (Part 1) by Gareth Dwyer

import json, logging, requests, time, urllib
from bs4 import BeautifulSoup
from lxml import html
import urllib.request
import gensim, logging
import time 
url = 'http://www.straitstimes.com/tags/fake-news?page={}'
base_url = 'http://www.straitstimes.com'

fake_news = {}

for page in range(1,3):
    text = urllib.request.urlopen(url.format(page)).read()
    soup = BeautifulSoup(text, 'lxml')
    for line in soup.select('.story-headline > a'):
        fake_news[line.string] = base_url + line['href']

print(fake_news)


# Rehurek, R.
# 2014, February 2
# Word2Vec Tutorial
# https://rare-technologies.com/word2vec-tutorial/
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', \
    level = logging.INFO)

# McCormick, C.
# 2016, April 12
# Google's trained Word2Vec model in Python
# http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/
start = time.time()
model = gensim.models.KeyedVectors.load_word2vec_format( \
    './GoogleNews-vectors-negative300.bin', binary = True)
inter = time.time()
print("TIME TO LOAD MODEL: %f" % (inter - start))

def getSimilarity(text0, text1):
    splittext0 = ''.join(ch for ch in text0 if ch.isalnum() or ch.isspace()).split()
    splittext1 = ''.join(ch for ch in text1 if ch.isalnum() or ch.isspace()).split()
    return model.n_similarity(splittext0, splittext1)

def getArticleScores(text):
    scores = {}
    for key in fake_news:
        scores[key] = getSimilarity(text, key)
        print(key + ' : ' + str(scores[key]))
    return scores

print(str(getArticleScores("Vivian Balakrishnan")))

# See https://docs.python.org/3/library/logging.html#logging.basicConfig for basicConfig options and
# https://docs.python.org/3/library/logging.html#logrecord-attributes for format options
logging.basicConfig(filename = 'bot.log', format = "%(asctime)s %(levelname)s %(message)s", level = logging.INFO)

with open('token.txt', 'r') as f:
    bot_token = f.readline().strip()

base_url = 'https://api.telegram.org/bot{}'.format(bot_token)

def get_json_from_url(url):
    response = requests.get(url)
    decoded_content = response.content.decode('utf-8')
    logging.info("GET %s responded with %s", url, decoded_content)
    return json.loads(decoded_content)

def get_updates(timeout, offset = None):
    url = '{}/getUpdates?timeout={}'.format(base_url, timeout)
    if offset:
        url += '&offset={}'.format(offset)
    return get_json_from_url(url)

def get_latest_update_id(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(int(update['update_id']))
    latest_update_id = max(update_ids)
    logging.info("get_latest_update_id: Latest update ID is %s of %s", latest_update_id, update_ids)
    return latest_update_id

def get_latest_chat_id_and_text(updates):
    text = updates['result'][-1]['message']['text'].encode('utf-8')
    chat_id = updates['result'][-1]['message']['chat']['id']
    logging.info("get_latest_chat_id_and_text: Latest message is %s from chat %s", text, chat_id)
    return (text, chat_id)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = '{}/sendMessage?text={}&chat_id={}&parse_mode=Markdown'.format(base_url, text, chat_id)
    logging.info("send_message: Sending %s to chat %s", text, chat_id)
    requests.get(url)

def handle_updates(updates, latest_update_id):
    for update in updates['result']:
        try:
            text = update['message']['text']
            chat = update['message']['chat']['id']
            sender = update['message']['from']['id']
            is_ascii = all(ord(char) < 128 for char in text)
            logging.info("handle_updates: Received %s from %s", text.encode('utf-8'), sender)

            if not is_ascii:
                logging.info("handle_updates: Block non-ascii message")
                send_message(replies['invalid'][0], chat)
                continue

            # Handle cases here
            print(str(chat) + " :: " + text)
            send_message('received!', chat)
            article_scores = getSimilarity(text, "Vivian Balakrishnan collapses at the UN")
            print(str(article_scores))
        except KeyError:
            pass

def main():
    latest_update_id = None
    while True:
        updates = get_updates(60, latest_update_id)
        if updates['result']:
            latest_update_id = get_latest_update_id(updates) + 1
            handle_updates(updates, latest_update_id)
        time.sleep(1)

if __name__ == '__main__':
    main()
