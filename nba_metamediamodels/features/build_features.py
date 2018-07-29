import requests
from bs4 import BeautifulSoup
import os
from html.parser import HTMLParser
import string

# organize this better
## TODO: don't keep repeating the same requests.get in every fn
## TODO: factor out some of the text processing functionality

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# def strip_ending_punc(string_):
#     count = 0
#     for l in string_[::-1]:
#         if l in string.punctuation:
#             count = count + 1
#     return string_[:count]

def get_title(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    cleantitle = strip_tags(str(soupdata.title)).strip()
    print(cleantitle)
    # translation = str.maketrans("", "", string.punctuation)
    # cleantitle_nopunc = cleantitle.translate(translation)
    # print(cleantitle_nopunc)

# for each link, get the text using this:
def get_body_text(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content,"html.parser")
    souptext = str(soupdata.find_all("div", class_="blog-body")[0])
    # print("")
    # print("THIS IS THE BLOG BODY CLASS")
    # print(type(souptext))
    # print(souptext)
    # print("")
    # print("THIS IS THE TEXT WITHOUT NEW LINES")
    nonewlinetext = souptext.replace('\n', ' ').replace('\r', '')
    # print(type(nonewlinetext))
    # print(nonewlinetext)
    cleansouptext = strip_tags(nonewlinetext).strip()
    # print("")
    # print("THIS IS THE CLEANED TEXT")
    # print(type(cleansouptext))
    print(cleansouptext)

def get_author(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    authortext = str(soupdata.find_all("a", class_="fn")[0])
    # authortext = str(soupdata.find_all("a", class_="fn",rel="author")[0])
    cleanauthortext = strip_tags(authortext).strip()
    print(cleanauthortext)

def get_publish_date(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    pubdate = str(soupdata.find_all("small", class_="byline")[0])
    nonewlinedate = pubdate.replace('\n', ' ').replace('\r', '')
    # print(pubdate)
    cleandate = strip_tags(nonewlinedate).strip()
    print(cleandate)

# get all the links from this page : http://grantland.com/contributors/zach-lowe/
def get_links(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content,"html.parser")
    for link in soupdata.find_all('a'):
        print(link.get('href'))

devurl = "http://grantland.com/the-triangle/five-minutes-with-bulls-coach-fred-hoiberg/"

get_body_text(devurl)

get_title(devurl)

get_author(devurl)

get_publish_date(devurl)

# get_soup_links("http://grantland.com/the-triangle/five-minutes-with-bulls-coach-fred-hoiberg/")
