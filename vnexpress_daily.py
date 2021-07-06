import requests
from bs4 import BeautifulSoup
import datetime
from dateutil import parser as date_parser
import mysql.connector
from datetime import datetime
from dateutil.parser import parse
from config import *
import threading

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
    
class VnExpewss():
    def main(self):
        for i in range(len(ARRAY_PAGE_VNEXPESS)):
            url_crawl = "https://e.vnexpress.net/category/listcategory/category_id/"+ARRAY_PAGE_VNEXPESS[i]+"/page/"
            self.main_crawl_data(url_crawl,i+1)
            print('Finish channel ',i+1)
        return
    def format_content(self,url_content):
        content = ''
        response = requests.get(url_content)   
        soup = BeautifulSoup(response.content, 'html.parser')
        fck_detail = soup.find('div',{'class':'fck_detail'})
        return fck_detail
    def format_date(self,time):
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
    def Thumbnail(self,item_news):
        img_link = item_news.find('img')
        return img_link['data-original']
    def crawl_data(self,url,page,channel_id):
        response = requests.get(url+str(page))
        json = response.json()
        soup = BeautifulSoup(json['html'], "html.parser")
        list_new = []
        for item_div in soup.find_all('div',{'class':'item_list_folder'}):
            item_news = item_div.find('div',{'class':'item_news'})
            #thumbnail
            thumbnail = self.Thumbnail(item_news)
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
            date_format = self.format_date(time)
            if date_format is None:
                continue
            #format content
            content = self.format_content(link['href'])
            if content is None:
                continue
            #kiểm tra title chưa có thì insert
            sql = "select * from news where title = %s and post_time = %s and channel_id = %s"
            title_sql = (title,date_format,channel_id,)
            mycursor.execute(sql, title_sql)
            myresult = mycursor.fetchall()
            if len(myresult) > 0:
                return 0
            data_news = (title,string_sub_title_str_format,str(content),date_now,date_now,date_format,channel_id,thumbnail)
            mycursor.execute(news, data_news)
            mydb.commit()
        return page
    def main_crawl_data(self,url_crawl,channel_id):
        i = 1
        while True:
            page = self.crawl_data(url_crawl,i,channel_id)
            sql = "select post_time from news where channel_id = %s ORDER BY post_time desc limit 1"
            channel_sql = (channel_id,)
            mycursor.execute(sql, channel_sql)
            myresult = mycursor.fetchall()
            if len(myresult) > 0:
                date_new = myresult[0][0]
                format_date_new = date_new.strftime("%Y-%m-%d")
                date_new = parse(format_date_new)
                date_crawl = parse('2021-05-01')
                if date_new < date_crawl:
                    print(date_new,'Finish')
                    return
            if page == 0:
                print('Finish')
                return
            if i ==  300:
                print('Finish')
                return
            i += 1
    