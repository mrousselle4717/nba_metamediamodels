import requests
from bs4 import BeautifulSoup
import os
from html.parser import HTMLParser
import string
import pandas as pd
import numpy as np
from dateutil import parser
import re
import configparser
# from selenium import webdriver
import time


# organize this better
## TODO: don't keep repeating the same requests.get in every fn
## TODO: factor out some of the text processing functionality
## TODO: need a get_site_name and get_raw_url and get_access_date func

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


# TODO: HUGE -- turn this whole thing into a class where the init holds the request, so it only happens once
# TODO: make unit tests for each of these funcs
# TODO: write good docstrings

"""
Plan here: 

start with https://www.theringer.com

an author's page looks like this: https://www.theringer.com/authors/zach-kram/archives/10

Then we can formulaically get our LINKSLIST for every author by creating all the urls (up to 100 or so),
and using our get_links() func to scrape each one for links.
To do this, we'll need to first have a list of all the ringer's writers (TODO: where to get this?)
Figure out a simple way to de-dup the list - maybe OrderedDict?

Then for each page in each author's list, we look for c-entry-content to get all the text


NEW PLAN:
use the ringer's nba archives
https://www.theringer.com/archives/nba/2016/12




"""

# TODO: figure out how to include this page http://www.espn.com/nba/news/archive/_/month/july/year/2015

# HERE - make a class which wraps all the below functions and uses the config file (and config parser) to turn the config into a dict and add those attributes:

# config = configparser.ConfigParser()
# config.read('html_config.ini')
# ringer_config = config._sections['theringer.com']
# print(ringer_config['link_name'])

        # 118
        # down vote
        # accepted
        # Sure, something like this:
        #
        # class Employee(object):
        #     def __init__(self, initial_data):
        #         for key in initial_data:
        #             setattr(self, key, initial_data[key])
        # Update
        #
        # As Brent Nash suggests, you can make this more flexible by allowing keyword arguments as well:
        #
        # class Employee(object):
        #     def __init__(self, *initial_data, **kwargs):
        #         for dictionary in initial_data:
        #             for key in dictionary:
        #                 setattr(self, key, dictionary[key])
        #         for key in kwargs:
        #             setattr(self, key, kwargs[key])
        # Then you can call it like this:
        #
        # e = Employee({"name": "abc", "age": 32})

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}

def get_title(url):
    thepage = requests.get(url,headers=headers)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    cleantitle = strip_tags(str(soupdata.title)).strip()
    print(cleantitle)
    return cleantitle
    # translation = str.maketrans("", "", string.punctuation)
    # cleantitle_nopunc = cleantitle.translate(translation)
    # print(cleantitle_nopunc)

# for each link, get the text using this:
def get_body_text(url):
    thepage = requests.get(url,headers=headers)
    soupdata = BeautifulSoup(thepage.content,"html.parser")
    # print(soupdata)
    # souptext = str(soupdata.find_all("div", class_="blog-body")[0])
    souptext = str(soupdata.find_all("div", class_="c-entry-content")[0])
    # souptext = soupdata.find_all("div", class_="c-entry-content")
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
    # print(cleansouptext)
    return cleansouptext

def get_author(url):
    thepage = requests.get(url,headers=headers)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    authortext = str(soupdata.find_all("span", class_="c-byline__item")[0])
    # authortext = str(soupdata.find_all("a", class_="fn",rel="author")[0])
    cleanauthortext = strip_tags(authortext).strip()
    print(cleanauthortext)
    return cleanauthortext

def get_publish_date(url):
    thepage = requests.get(url,headers=headers)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    pubdate = str(soupdata.find_all("time", class_="c-byline__item")[0])
    nonewlinedate = pubdate.replace('\n', ' ').replace('\r', '')
    # print(pubdate)
    cleandate = strip_tags(nonewlinedate).strip()
    formatteddate = parser.parse(cleandate)
    print(formatteddate)
    return formatteddate

# get all the links from this page : http://grantland.com/contributors/zach-lowe/
def get_links(url):
    thepage = requests.get(url,headers=headers)
    soupdata = BeautifulSoup(thepage.content,"html.parser")
    # print(soupdata)
    links1 = soupdata.find_all("h2", class_="c-entry-box--compact__title")
    print(links1)
    links2 = []
    for i in np.arange(0,len(links1)):
        test = re.findall('"([^"]*)"',str(links1[i]))[-1]
        # print(str(links1[i]))
        links2.append(test)
        # print(test)
    # links2 = []
    # for i in range(len(links1)):
    #     address = links1[i].get('href')
    #     links2.append(address)
    links = []
    # for i in links1:
    #     links.append(i.get('href'))
    print(links2)
    return links2
    # links = []
    # for link in soupdata.find_all('a'):
    #     links.append(link.get('href'))
    # print(links)
    # return links



if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('html_config.ini')
    ringer_config = config._sections['theringer.com']
    print(ringer_config['link_name'])
    # site = 'theringer'

    # better string formatting - "f" strings

    # rooturl = f"http://www.{site}.com/"
    #
    # devurl = f"{rooturl}nba/2018/7/27/17620472/lebron-james-murals-los-angeles-lakers-kobe-bryant"
    #
    # textlist = [get_body_text(devurl)]
    #
    # titlelist = [get_title(devurl)]
    #
    # authorlist = [get_author(devurl)]
    #
    # datelist = [get_publish_date(devurl)]
    #
    # urllist = [devurl]
    #
    # sitelist = [site]

    # get_soup_links("http://grantland.com/the-triangle/five-minutes-with-bulls-coach-fred-hoiberg/")

    # make the dataframe

    # data = pd.DataFrame({'author': authorlist,
    #                        'site': sitelist,
    #                        'date': datelist,
    #                        'title': titlelist,
    #                        'body': textlist,
    #                        'url':urllist
    #                      })
    # print(data.info())
    # print(data.head().T)
    #
    # linkslist = get_links("https://www.theringer.com/archives/nba/2016/12")
    #
    #
    # print(len(linkslist))
