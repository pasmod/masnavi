from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2
import selectors
import codecs
import os


def _get_page_urls(base_url, selector=selectors.PAGE_URL_SELECTOR):
    response = urllib2.urlopen(base_url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    hrefs = [el.get('href') for el in soup.select(selector)]
    urls = [urljoin(base_url, href) for href in hrefs]
    return urls


def get_poem_urls(base_url, selector=selectors.POEM_URL_SELECTOR):
    page_urls = _get_page_urls(base_url)
    poem_urls = []
    for page_url in page_urls:
        response = urllib2.urlopen(page_url)
        soup = BeautifulSoup(response.read(), 'html.parser')
        hrefs = [el.get('href') for el in soup.select(selector)]
        urls = [urljoin(base_url, href) for href in hrefs]
        poem_urls.extend(urls)
    return poem_urls


def write_poem_urls(poem_urls, filename='poem_urls.txt'):
    with codecs.open(filename, 'w', 'utf-8') as outfile:
        for url in poem_urls:
            outfile.write(url)
            outfile.write('\n')


def read_poem_urls(urlsfile):
    urls = []
    with codecs.open(urlsfile, 'r', 'utf-8') as infile:
        for line in infile:
            urls.append(line.rstrip('\n'))
    return urls


def extract_poem(poem_url, selector=selectors.POEM_CONTENT):
    response = urllib2.urlopen(poem_url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    couplets = [[el.select('div.m1 p')[0].text,
                 el.select('div.m2 p')[0].text]
                for el in soup.select(selector)]
    return couplets


def write_poem(poem, filename):
    with codecs.open(filename, 'w', 'utf-8') as outfile:
        for couplet in poem:
            for m in couplet:
                outfile.write(m)
                outfile.write('\n')


def read_poems(folder):
    poems = []
    for root, directories, files in os.walk(folder):
        for filename in files:
            filepath = os.path.join(root, filename)
            with codecs.open(filepath, 'r', 'utf-8') as infile:
                poem = []
                for line in infile:
                    poem.append(line.rstrip('\n'))
                poems.append(poem)
    return poems


if __name__ == "__main__":
    poem_urls = read_poem_urls('data/ferdousi/shahname/shahname.urls')
    for url in poem_urls:
        poem = extract_poem(url)
        write_poem(poem, url.split('/')[-3] + '_' + url.split('/')[-2] + '.txt')
