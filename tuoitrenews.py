# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 12:46:17 2021

@author: ADMIN
"""
import re
import requests
from bs4 import BeautifulSoup

r = requests.get("https://tuoitrenews.vn/society") 
data = r.content  # Content of response
soup = BeautifulSoup(data, "html.parser")
for item_div in soup.find_all('div',{'class':'item_list_folder'}):
    item_news = item_div.find('div',{'class':'item_news'})
    if item_news is None:
        continue
    i = item_news.find('h2',{'class':'title_news_site'})
    link = i.find('a',href=True)
    if link is None:
        continue
    print(link['title'])