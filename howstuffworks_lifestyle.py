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
import pandas as pd 

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
    response = requests.get(url_content)   
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('div',{'id':'content-well'})
    if body is None:
        return
    date_text = body.find('p',{'class':'text-muted'})
    if date_text is None:
        date_text = body.find('span',{'class':'content-date'})
    if date_text is None:
        return
    
    if 'Originally Published:' in date_text.text:
        date = format_date(date_text.text.replace('Originally Published: ',''))
    if 'Updated: ' in date_text.text:
        date = format_date(date_text.text.replace('Updated: ',''))
    if 'Updated: ' not in date_text.text and 'Originally Published:' not in date_text.text:
         date = format_date(date_text.text)
    content = body.find('div',{'class':'page-body'})
    content_date ={
        "date" : date,
        "content" : content,
        }
    return content_date
def format_date(time):
    date = date_parser.parse(time)
    date_format = date.strftime("%Y-%m-%d %H:%M:%S")
    return date_format
def crawl_data(link,channel_id):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find('div',{'id':'landing-content'})
    for item_div in body.find_all('div',{'class':'flex-col'}):
        thumbnail = item_div.find('img',{'class':'img-fluid'})['data-src']
        title_content = item_div.find('div',{'class':'text-xl'})
        content_url = title_content.find('a',href=True)
        content_date = format_content(content_url['href'])
        if content_date is None:
            continue
        date_format = content_date['date']
        content = content_date['content']
        title = title_content.text
        sub_title = item_div.find('p',{'class':'text-black'}).text
        sql = "select * from news where title = %s and post_time = %s"
        title_sql = (title,date_format,)
        mycursor.execute(sql, title_sql)
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            print(len(myresult),"error sql")
            continue
        data_news = (title,sub_title,str(content),date_now,date_now,date_format,channel_id,thumbnail)
        mycursor.execute(news, data_news)
        mydb.commit()
    return
def main_crawl_data():
    channel_id = 9
    array_page = ['home','entertainment','lifestyle']
    for index in array_page:
        response = requests.get('https://'+index+'.howstuffworks.com/')
        soup = BeautifulSoup(response.content, "html.parser")
        body = soup.find('div',{'id':'landing-content'})
        array_link = []
        for item in body.find_all('div',{'class':'mb-10'}):
            link = item.find('a',{'class':'text-primary'})
            array_link.append(link['href'])
        for link in array_link:
            page = crawl_data(link,channel_id)
    print('Finish')
    return
if __name__ == '__main__':
    main_crawl_data()
    
    