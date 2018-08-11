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
import pprint
from datetime import datetime
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
use the ringer's nba archives -- and rather than SCRAPING the links, CONSTRUCT the links via the following formula:
https://www.theringer.com/archives/nba/2016/12
"""

# TODO: figure out how to include this page http://www.espn.com/nba/news/archive/_/month/july/year/2015

# TODO: MORE IDEAS FOR HOW TO FINISH THIS CLASS:
"""
"""

# I think we're resigned to making 2 classes here, one to get links for any site,
# and one that uses links to gather data.
# Further, the first class here will be unfortunately ugly -- it'll HAVE to contain a specialized,
# function for each website; I can't figure out a way to do this through the config file.

class NBAColumnCollector(object):
    def __init__(self,
                 article_links_list=[]
                 ):
        pass
    def get_ringer_links(self):
        pass

    @staticmethod
    def get_max_monthyear():
        today = datetime.today()
        m_y_tup = (today.month,today.year)
        return m_y_tup




class NBAScraper(object):
    """
    A class that scrapes a few pieces of information from NBA websites, using an associated config file.

    This class should be instantiated TWICE with the same config file for its use (not sure this is the best design)
    - the first instance should aim to fill the self._article_links_list attribute with a list of all the links
        on a specific site that we want to scrape

    TODO: fill this in
    """
    def __init__(self,
                 config_file,
                 config_section,
                 article_links_list,
                 headers=None
                 ):
        # the following attrs have leading _'s to keep the passed arguments separate from the attrs
        self._config_file=config_file
        self._config_section=config_section
        self._article_links_list=article_links_list  # fill in with something like self.get_all_links
        self._headers=headers
        self._config_dict = self._load_config_dict(self._config_file,self._config_section)
        self._assign_attrs_from_config(self._config_dict)

        # boilerplate headers - required only to complete the transaction
        # TODO: add if statement - if passed in, then check them and take those, if not use these
        self._headers = {
                            'User-Agent': 'My User Agent 1.0',
                            'From': 'youremail@domain.com'  # This is another valid field
                        }

    def _load_config_dict(self, config_file, config_section):
        config = configparser.ConfigParser()
        config.read(config_file)
        config_dict = config._sections[config_section]
        return config_dict

    def _assign_attrs_from_config(self,config_dict):
        for key in config_dict:
            setattr(self, key, config_dict[key])

    @staticmethod
    def make_request(url, headers):
        # uses requests lib to make the request
        thepage = requests.get(url, headers)
        return thepage

    @staticmethod
    def get_content(http_response):
        # returns the content of the http request
        contents = http_response.content
        return contents

    @staticmethod
    def parse_html(http_response_content):
        soupdata = BeautifulSoup(http_response_content, "html.parser")
        return soupdata

    @staticmethod
    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    # I DON"T THINK THIS IS GOING TO WORK - NESTED FSTRINGS ARENT POSSIBLE (apparently!)
    def _construct_test_link_from_config(self):

        test_link = str(self.archivepath)
        return f"{test_link}"

    def _construct_links_from_config(self):
        pass

    # @staticmethod
    # def create_url_from_root(rooturl, archivepath, archive_start_month, archive_start_year):
    #
    #
    # def get_all_links(self,):

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

# NOTE: THERE SHOULD BE 2 WAYS TO GET LINKS
# -- one is to scrape one INDEX page of a site for all its links, deduping some and throwing junk away
# -- two is to use details in the config file to CONSTRUCT links
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
    # testnba = NBAScraper(config_file='html_config.ini', config_section='theringer.com')
    # attrs = vars(testnba)
    # {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
    # now dump this in some way or another
    # pprint.pprint(attrs) # print it nice
    # print(testnba)

    cc = NBAColumnCollector()

    print(cc.get_max_monthyear())


    # config = configparser.ConfigParser()
    # config.read('html_config.ini')
    # ringer_config = config._sections['theringer.com']
    # print(ringer_config['link_name'])
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
