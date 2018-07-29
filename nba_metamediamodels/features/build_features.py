import requests
from bs4 import BeautifulSoup
import os
from html.parser import HTMLParser
import string
import pandas as pd
import numpy as np
from dateutil import parser
import re
from selenium import webdriver
import time

driver = webdriver.PhantomJS(executable_path='')
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")

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

def get_title(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    cleantitle = strip_tags(str(soupdata.title)).strip()
    print(cleantitle)
    return cleantitle
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
    return cleansouptext

def get_author(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    authortext = str(soupdata.find_all("a", class_="fn")[0])
    # authortext = str(soupdata.find_all("a", class_="fn",rel="author")[0])
    cleanauthortext = strip_tags(authortext).strip()
    print(cleanauthortext)
    return cleanauthortext

def get_publish_date(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content, "html.parser")
    pubdate = str(soupdata.find_all("small", class_="byline")[0])
    nonewlinedate = pubdate.replace('\n', ' ').replace('\r', '')
    # print(pubdate)
    cleandate = strip_tags(nonewlinedate).strip()
    formatteddate = parser.parse(cleandate)
    print(formatteddate)
    return formatteddate

# get all the links from this page : http://grantland.com/contributors/zach-lowe/
def get_links(url):
    thepage = requests.get(url)
    soupdata = BeautifulSoup(thepage.content,"html.parser")
    # print(soupdata)
    links1 = soupdata.find_all("h3", class_="headline beta")
    print(links1)
    for i in np.arange(0,len(links1)):
        test = re.findall('"([^"]*)"',str(links1[i]))
        # print(str(links1[i]))
        print(test)
    # links2 = []
    # for i in range(len(links1)):
    #     address = links1[i].get('href')
    #     links2.append(address)
    links = []
    # for i in links1:
    #     links.append(i.get('href'))
    # print(links2)
    # return links2
    # links = []
    # for link in soupdata.find_all('a'):
    #     links.append(link.get('href'))
    # print(links)
    # return links



if __name__ == '__main__':
    site = 'grantland'

    # better string formatting - "f" strings

    rooturl = f"http://{site}.com/"

    devurl = f"{rooturl}the-triangle/five-minutes-with-bulls-coach-fred-hoiberg/"

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

    # linkslist = get_links("http://grantland.com/contributors/zach-lowe/")
    url = "http://grantland.com/contributors/zach-lowe/"
    driver = webdriver.PhantomJS()
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    page_num = 0

    while driver.find_elements_by_css_selector('.search-result-more-txt'):
        driver.find_element_by_css_selector('.search-result-more-txt').click()
        page_num += 1
        print("getting page number " + str(page_num))
        time.sleep(1)

    html = driver.page_source.encode('utf-8')


    # print(len(linkslist))
