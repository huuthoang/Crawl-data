# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 15:22:34 2021

@author: ADMIN
"""


import requests
from bs4 import BeautifulSoup
import datetime
from dateutil import parser as date_parser
import mysql.connector
from datetime import datetime
from dateutil.parser import parse
from config import *

url = "https://e.vnexpress.net/category/listcategory/category_id/1003894/page/"
now = datetime.now()
date_now = now.strftime("%Y/%m/%d %H:%M:%S")
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="123456",
  database="bosscake"
)
mycursor = mydb.cursor()
news = """INSERT INTO news 
        (title,
         sub_title,
         content,
         created_at,
         updated_at,
         post_time,
         channel_id,
         thumbnail) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
def format_content(url_content):
    content = ''
    response = requests.get(url_content)   
    soup = BeautifulSoup(response.content, 'html.parser')
    fck_detail = soup.find('div',{'class':'fck_detail'})
    return fck_detail
# =============================================================================
#     for item_div in fck_detail.find_all('p',{'class':'Normal'}):
#         if item_div is None:
#             continue
#         if content == '':
#             content = item_div.text
#         content = content+item_div.text
#     return content
# =============================================================================
def format_date(time):
    sring = time.text.replace("\n", "")
    string_date = sring.replace("  ", "")
    x = "|" not in string_date
    if x == False:
        string_date = sring.replace("|", "")
    if "GMT+7" not in string_date:
        return None
    date = date_parser.parse(string_date)
    date_format = date.strftime("%Y-%m-%d %H:%M:%S")
    return date_format
def Thumbnail(item_news):
    img_link = item_news.find('img')
    return img_link['data-original']
def crawl_data(page):
    response = requests.get(url+str(page))
    json = response.json()
    soup = BeautifulSoup(json['html'], "html.parser")
    list_new = []
    for item_div in soup.find_all('div',{'class':'item_list_folder'}):
        item_news = item_div.find('div',{'class':'item_news'})
        #thumbnail
        thumbnail = Thumbnail(item_news)
        #content
        sub_title = item_news.find('div',attrs={'class':'lead_news_site'})
        sub_title_str = sub_title.find('a',href=True)
        if sub_title_str is None:
            continue
        string_sub_title = sub_title_str.text.replace("\n", "")
        string_sub_title_str_format = string_sub_title.replace("										", "")
        
        if item_news is None:
            continue
        i = item_news.find('h2',{'class':'title_news_site'})
        link = i.find('a',href=True)
        if link is None:
            continue
        #title 
        title = link['title'].replace("				", "")
        time = item_div.find('div',{'class':'timer_post'})
        date_format = format_date(time)
        if date_format is None:
            continue
        
        #format content
        content = format_content(link['href'])
        if content is None:
            continue
        #kiểm tra title chưa có thì insert
        sql = "select * from news where title = %s"
        title_sql = (title,)
        mycursor.execute(sql, title_sql)
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            print(myresult)
            return 0
        data_news = (title,string_sub_title_str_format,str(content),date_now,date_now,date_format,CHANNEL_ID_VNEXPRESS,thumbnail)
        mycursor.execute(news, data_news)
       
        mydb.commit()
    return page
def main_crawl_data():
    i = 1
    while True:
        page = crawl_data(i)
        mycursor.execute("select post_time from news ORDER BY post_time asc limit 1")
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            date_new = myresult[0][0]
            format_date_new = date_new.strftime("%Y-%m-%d")
            date_new = parse(format_date_new)
            date_crawl = parse('2021-05-01')
            if date_new < date_crawl:
                print('Finish')
                return
        if page == 0:
            print('Finish')
            return
        i += 1
if __name__ == '__main__':
    main_crawl_data()
