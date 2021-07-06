# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 11:05:22 2021

@author: ADMIN
"""

import requests
from bs4 import BeautifulSoup
import datetime
from dateutil import parser as date_parser
import mysql.connector
from datetime import datetime
from dateutil.parser import parse
from threading import Thread
import threading
import time
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
    url = "https://tuoitrenews.vn"
    response = requests.get(url+url_content)   
    soup = BeautifulSoup(response.content, 'html.parser')
    art_header = soup.find('article',{'class':'art-header'})
    #date format
    date = format_date(art_header.find('div',{'class':'date'}).text)
    #content
    art_content = soup.find_all('div',{'class':'row-1'})[1] 
    content = art_content.find_all('div',{'id':'content-body'})
    content_date ={
        "date" : date,
        "content" : content,
        }
    return content_date
def format_date(time):
    date = date_parser.parse(time)
    date_format = date.strftime("%Y-%m-%d %H:%M:%S")
    return date_format
def thread(item_div,channel_id):
    print("calculate square number")
    hasComment = item_div.find('h3',{'class':'hasComment'})
    title = hasComment.find('a',href=True)['title']
    sub_title = item_div.find('p').text
    thumbnail = item_div.find('img')['src']
    content_date = format_content(item_div.find('a',href=True)['href'])
    date_format = content_date['date']
    content = content_date['content']
    sql = "select * from news where title = %s and post_time = %s"
    title_sql = (title,date_format,)
    mycursor.execute(sql, title_sql)
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        print(len(myresult),"error sql")
        return
    data_news = (title,sub_title,str(content[0]),date_now,date_now,date_format,channel_id,thumbnail)
    mycursor.execute(news, data_news)
    mydb.commit()
    return
def crawl_data(page,channel_id):
    try:
        url = "https://tuoitrenews.vn/page?slug=ttn-lifestyle&ajax=13---ttnews_custom_list&page_number="+str(page)
        headers = {
            'authority':'tuoitrenews.vn',
            'sec-ch-ua' : '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'accept':'*/*',
            'x-csrf-token':'tuWzJFCI7Cbjrd3f72nnsnv_rwk2MvW0_mFLjEbyjSrF3IF2Nb2qcoWfh63ZXaTtTq_HPnxYvuK3NC-4IaPCfg==',
            'sec-ch-ua-mobile':'?0',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'x-requested-with':'XMLHttpRequest',
            'sec-fetch-site':'same-origin',
            'sec-fetch-mode':'cors',
            'sec-fetch-dest':'empty',
            'referer':'https://tuoitrenews.vn/society',
            'accept-language':'en-US,en;q=0.9,vi;q=0.8',
            'cookie':'_uidcms=162485369825987510; _ga=GA1.2.1238474114.1624853699; __RC=5; __R=3; __gads=ID=3ed3e093827f415c:T=1624853700:S=ALNI_MY7Se-LfyI2E2k4fWCwWXN0hSAmTQ; __tb=0; fg_version=3; fg_uuid=0f8975a6d023e0a6114b20b196d85618; __UF=2%2C5; fg_lastUpdate=1625210811094; _gid=GA1.2.935057992.1625453099; __IP=1953376312; _gat_UA-9712051-40=1; __uif=__uid%3A1860848272112614305%7C__ui%3A2%252C5%7C__create%3A1616084827; fg_lastModify=1625538942726; fg_guid=8660848272112614305'
            }
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.json()['data'], 'html.parser')
        list_news_content = soup.find('div',{'class':'list-news-content'})
        for item_div in soup.find_all('article',{'class':'art-lastest'}):
            t = time.time()
            t1 = threading.Thread(target=thread, args=(item_div,channel_id,))
            t1.start()
            t1.join()
        return
    except ValueError as error:
        print(error)
        pass
    
def main_crawl_data():
    i = 0
    #channel lifestyle
    channel_id = 6
    while True:
        sql = "select post_time from news where channel_id = %s ORDER BY post_time asc limit 1"
        channel_sql = (channel_id,)
        mycursor.execute(sql, channel_sql)
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            date_new = myresult[0][0]
            format_date_new = date_new.strftime("%Y-%m-%d")
            date_new = parse(format_date_new)
            date_crawl = parse('2021-05-01')
            if date_new < date_crawl:
                print(date_new)
                print('Finish')
                return
        crawl_data(i,channel_id)
        i +=1
        print("Success")
if __name__ == '__main__':  
    main_crawl_data()