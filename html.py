# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 11:08:28 2021

@author: ADMIN
"""

import requests
from bs4 import BeautifulSoup

# Make a request
page = requests.get(
    "https://e.vnexpress.net/news/news/vietnam-shortens-synthesis-of-covid-antiviral-4301366.html")
soup = BeautifulSoup(page.content, 'html.parser')

# Extract title of page
page_title = soup.title

# Extract body of page
page_body = soup.body

# Extract head of page
page_head = soup.head

# print the result
print(page_body)