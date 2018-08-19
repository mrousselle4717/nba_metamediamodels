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
from dateutil.rrule import rrule, MONTHLY
from datetime import datetime

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
# TODO: add type hints to all the functions here
# TODO: make a factory method under NBASCRAPER called make_ringer(cls) which will return an instance of NBASCRAPER prepopulated with the ringer materials (think about the margerhita pizza example)
# TODO: use the hypothesis library to do testing like this: https://hillelwayne.com/talks/beyond-unit-tests/ &  https://hypothesis.readthedocs.io/en/latest/quickstart.html & https://github.com/deadpixi/contracts
# TODO: add type-hints to all these functions & run mypy against it
# TODO: when deploying, use this resource: http://flask.pocoo.org/docs/1.0/deploying/

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

# TODO: add a base class here that both these below classes will inherit from so we don't have to repeat so much code

class NBAScraperBase(object):
    """
        A base class with all boilerplate functionality to do web scraping/parsing using params from a config file
    """
    def __init__(self,
                 config_file,
                 config_section,
                 headers=None
                 ):
        # the following attrs have leading _'s to keep the passed arguments separate from the attrs
        self._config_file=config_file
        self._config_section=config_section
        self._article_link=article_link
        self._config_dict = self.load_config_dict(self._config_file,self._config_section)
        self._assign_attrs_from_config(self._config_dict)

        # boilerplate headers - required only to complete the transaction
        # TODO: add if statement - if passed in, then check them and take those, if not use these
        self._headers=headers
        self._headers = {
                            'User-Agent': 'My User Agent 1.0',
                            'From': 'youremail@domain.com'  # This is another valid field
                        }

    def load_config_dict(self, config_file, config_section):
        """
            Loads our custom .ini config file using configparser (in the standard library)
            We'll use this method to assign the private attribute ._config_dict
        :param config_file: .ini file, or any file that won't error with configparser.ConfigParser().read(FILE)
        :param config_section: str, the _sections[] header within the config file containing our required params
        :return: dict, key-value pairs of all elements in the specified section of the config file
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        config_dict = config._sections[config_section]
        return config_dict

    def _assign_attrs_from_config(self,config_dict):
        """
            Private method to take any dictionary and perform 2 operations:
                1) turn the keys of that dict into named attributes of the instance
                2) set the values of that dict to their associated attributes (formerly, associated keys)
        :param config_dict: dict, usually one from a config file
        :return: nothing is returned; instance attributes are set
        """
        for key in config_dict:
            setattr(self, key, config_dict[key])


class NBAColumnCollector(object):
    def __init__(self,
                 config_file,
                 config_section,
                 pages_to_scrape_for_links=[],
                 article_links_list=[],
                 headers=None
                 ):
        # the following attrs have leading _'s to keep the passed arguments separate from the attrs
        self._config_file = config_file
        self._config_section = config_section
        self._pages_to_scrape_for_links = pages_to_scrape_for_links  # fill in with something like self.get_all_links
        self._article_links_list = article_links_list
        self._headers = headers
        self._config_dict = self._load_config_dict(self._config_file, self._config_section)
        self._assign_attrs_from_config(self._config_dict)

        # boilerplate headers - required only to complete the transaction
        # TODO: add if statement - if passed in, then check them and take those, if not use these
        self._headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.com'  # This is another valid field
        }
    def get_ringer_links(self):
        pass

    def _load_config_dict(self, config_file, config_section):
        config = configparser.ConfigParser()
        config.read(config_file)
        config_dict = config._sections[config_section]
        return config_dict

    def _assign_attrs_from_config(self,config_dict):
        for key in config_dict:
            setattr(self, key, config_dict[key])

    @staticmethod
    def get_max_monthyear():
        today = datetime.today()
        m_y_tup = (today.month,today.year)
        return m_y_tup

    @staticmethod
    def make_month_year_tuple_list(start_month, start_year, end_month, end_year):
        start = datetime(start_year, start_month, 1)
        end = datetime(end_year, end_month, 1)
        return [(d.month, d.year) for d in rrule(MONTHLY, dtstart=start, until=end)]

    def make_ringer_linkfilled_pages(self):
        end_month, end_year = self.get_max_monthyear()
        self.archive_end_month = end_month
        self.archive_end_year = end_year
        m_y_list = self.make_month_year_tuple_list(int(self.archive_start_month),
                                                   int(self.archive_start_year),
                                                   self.archive_end_month,
                                                   self.archive_end_year)
        for (m,y) in m_y_list:
            link = self.rooturl+self.archive_path_prefix+str(y)+'/'+str(m)
            # print(link)
            self._pages_to_scrape_for_links.append(link)

    @staticmethod
    def get_links_from_page(page_url,my_headers,link_name,link_class):
        thepage = requests.get(url=page_url,headers=my_headers)
        soupdata = BeautifulSoup(thepage.content,"html.parser")
        all_links = soupdata.find_all(link_name, class_=link_class)
        links = []
        for i in np.arange(0,len(all_links)):
            clean_link = re.findall('"([^"]*)"',str(all_links[i]))[-1]
            links.append(clean_link)
        return links

    def get_links_from_all_linkfilled_pages(self):
        # add a state-ful check here to make sure that the instance of the class has already run
        # self.make_ringer_linkfilled_pages(), or maybe that the self._pages_to_scrape_for_links isn't empty
        # might be good to say "warning, you haven't gotten the linkfilled pages yet, but if you're confident the
        # links you entered into pages_to_scrape_for_links=[] is good, then we can go ahead and scrape the links
        for linkfilled_page in self._pages_to_scrape_for_links:
            page_links = self.get_links_from_page(linkfilled_page,
                                                  self._headers,
                                                  self.link_name,
                                                  self.link_class
                                                  )
            # print(page_links)
            self._article_links_list = self._article_links_list + page_links

        # dedup
        self._article_links_list = list(set(self._article_links_list))

        # and a list comp to remove all podcasts:
        self._article_links_list = [x for x in self._article_links_list if "podcast" not in x.lower()]


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
                 article_link,
                 headers=None
                 ):
        # the following attrs have leading _'s to keep the passed arguments separate from the attrs
        self._config_file=config_file
        self._config_section=config_section
        self._article_link=article_link
        self._headers=headers
        self._config_dict = self.load_config_dict(self._config_file,self._config_section)
        self._assign_attrs_from_config(self._config_dict)

        # boilerplate headers - required only to complete the transaction
        # TODO: add if statement - if passed in, then check them and take those, if not use these
        self._headers = {
                            'User-Agent': 'My User Agent 1.0',
                            'From': 'youremail@domain.com'  # This is another valid field
                        }

    @staticmethod
    def load_config_dict(config_file, config_section):
        """
            Loads our custom .ini config file using configparser (in the standard library)
            We'll use this method to assign the private attribute ._config_dict
        :param config_file: .ini file, or any file that won't error with configparser.ConfigParser().read(FILE)
        :param config_section: str, the _sections[] header within the config file containing our required params
        :return: dict, key-value pairs of all elements in the specified section of the config file
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        config_dict = config._sections[config_section]
        return config_dict

    def _assign_attrs_from_config(self,config_dict):
        """
            Private method to take any dictionary and perform 2 operations:
                1) turn the keys of that dict into named attributes of the instance
                2) set the values of that dict to their associated attributes (formerly, associated keys)
        :param config_dict: dict, usually one from a config file
        :return: nothing is returned; instance attributes are set
        """
        for key in config_dict:
            setattr(self, key, config_dict[key])

    @staticmethod
    def make_request(url, headers):
        """
            Uses the requests library and invokes requests.get() with the passed arguments to access HTTP endpoint
        :param url: str, an http address to which you'd like to direct a GET request
        :param headers: dict, filled with minimum criteria for making a request (need 'User-Agent' and 'From' keys)
        :return: object, the GET response using format from the requests lib
        """
        thepage = requests.get(url, headers)
        return thepage

    @staticmethod
    def get_content(http_response):
        """
            Returns content from an HTTP GET response; this content can then be parsed using any HTML parser.
            Here, we'll use BS4 to do the parsing.
        :param http_response: object, a GET response using format from the requests lib
        :return: the .content (syntax from the requests lib) from an HTTP response
        """
        contents = http_response.content
        return contents

    @staticmethod
    def parse_html(http_response_content):
        """
            Uses BS4 and the "html.parser" to turn the GET response's content into text.
            We'll parse actual information out of this text later.
        :param http_response_content: the .content (syntax from the requests lib) from an HTTP response
        :return: obj, a BS4 html parsed object that we can either convert to text or search through methodically
        """
        soupdata = BeautifulSoup(http_response_content, "html.parser")
        return soupdata

    @staticmethod
    def strip_tags(html):
        """
            A helper method to clean up post-parsed web text; often, this text will still have some html tags in it,
            And this is a simple way to remove them all.
        :param html: str, any text string with standardized html code in it that we'd like to filter out
        :return: str, a text string WITHOUT any html tags
        """
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    @staticmethod
    def get_title(parsed_html_content):
        """
            Takes a text string, assumed to be
        :param parsed_html_content: obj, the returned data from BS4's html parser
        :return: str, the title attribute from BS4's post-html-parser, w/o html tags, and converted to string
        """
        # remove the html crap
        cleantitle = strip_tags(str(parsed_html_content.title)).strip()
        return cleantitle

    @staticmethod
    def get_body_text(parsed_html_content,body_name,body_class):
        # return the body text using pre-defined search params, and take the first item in the returned list (should only ever be 1 item)
        souptext = str(parsed_html_content.find_all(body_name, class_=body_class)[0])
        # replace new lines
        nonewlinetext = souptext.replace('\n', ' ').replace('\r', '')
        # remove the html code crap
        cleansouptext = strip_tags(nonewlinetext).strip()
        return cleansouptext

    @staticmethod
    def get_author(parsed_html_content,author_name,author_class):
        """
            Get the author's name using pre-defined search params,
            and take the first item in the returned list (should only ever be 1 item)
        :param parsed_html_content: object, Html parsed BS4 object
        :param author_name: str, the name of the html key (found in our config file) for author name
        :param author_class: str, the input for the `class_` arg in BS4's .find_all() for author name (in config file)
        :return: str, author name
        """
        authortext = str(parsed_html_content.find_all(author_name, class_=author_class)[0])
        # remove the html code crap
        cleanauthortext = strip_tags(authortext).strip()
        return cleanauthortext

    @staticmethod
    def get_publish_date(parsed_html_content,pubdate_name,pubdate_class):
        """
            Get publish date using pre-defined search params,
            and take the first item in the returned list (should only ever be 1 item)
        :param parsed_html_content: object, Html parsed BS4 object
        :param pubdate_name: str, the name of the html key (found in our config file) for publish date
        :param pubdate_class: str, the input for the `class_` arg in BS4's .find_all() for publish date (in config file)
        :return: dt, publish date
        """
        pubdate = str(parsed_html_content.find_all(pubdate_name, class_=pubdate_class)[0])
        # replace new lines
        nonewlinedate = pubdate.replace('\n', ' ').replace('\r', '')
        # remove the html code crap
        cleandate = strip_tags(nonewlinedate).strip()
        formatteddate = parser.parse(cleandate)
        return formatteddate

    @staticmethod
    def make_series_from_components(title, author, website, publish_date, body_text):
        retrieval_date = datetime.today()
        features_dict = {'title':title,
                         'author':author,
                         'website':website,
                         'publish_date':publish_date,
                         'body':body_text,
                         'retrieval_date':retrieval_date

                        }
        features_series = pd.Series(features_dict)
        return features_series
    # TODO: add method to create a series (with a dict inside) like this: pandas.Series({'a':1, 'b':5, 'c':2, 'd':3})
    #       so that the top level function of this class will return an object that a loop can consume
    #       and fill a dataframe with, using loc: https://stackoverflow.com/questions/17091769/python-pandas-fill-a-dataframe-row-by-row



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

    cc = NBAColumnCollector(config_file='html_config.ini',
                            config_section='theringer.com'
                            )

    cc.make_ringer_linkfilled_pages()
    # pprint.pprint(cc._pages_to_scrape_for_links)

    cc.get_links_from_all_linkfilled_pages()
    print(len(cc._article_links_list))
    # pprint.pprint(cc._article_links_list)

    scraper = NBAScraper(config_file='html_config.ini',
                         config_section='theringer.com',
                         article_links_list=cc._article_links_list
                         )


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
