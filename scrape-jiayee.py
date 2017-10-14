from bs4 import BeautifulSoup
from lxml import html
import urllib.request

url = 'http://www.straitstimes.com/tags/fake-news?page={}'

page = 1
text = urllib.request.urlopen(url.format(page)).read()
soup = BeautifulSoup(text, 'lxml')

for line in soup.select('.story-headline > a'):
    print(line['href'], line.string)
