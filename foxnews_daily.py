import requests
from bs4 import BeautifulSoup
import datetime
from dateutil import parser as date_parser
import mysql.connector
from datetime import datetime
from dateutil.parser import parse
from config import CHANNEL_ID_FOXNEWS
import time
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
class Foxnews():
    def main(self):
        self.main_crawl_data()
        return
    def format_content(self,url_content):
        url = "https://www.foxnews.com"
        response = requests.get(url+url_content)   
        soup = BeautifulSoup(response.content, 'html.parser')
        main_detail_page = soup.find('div',{'class':'article-content'})
        return main_detail_page
    def format_date(self,time):
        date = date_parser.parse(time)
        date_format = date.strftime("%Y-%m-%d %H:%M:%S")
        return date_format
    def cal_square(self,obj,channel_id):
        thumbnail = obj['imageUrl']
        title = obj['title']
        sub_title = obj['description']
        date_format = self.format_date(obj['lastPublishedDate'])
        if "https://" in obj['url']:
            print("error link")
            return None
        content = self.format_content(obj['url'])
        sql = "select * from news where title = %s and post_time = %s and channel_id = %s"
        title_sql = (title,date_format,channel_id,)
        mycursor.execute(sql, title_sql)
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            print(len(myresult),"error sql")
            return None
        data_news = (title,sub_title,str(content),date_now,date_now,date_format,channel_id,thumbnail)
        mycursor.execute(news, data_news)
        mydb.commit()
        return
    def crawl_data(self,url,channel_id):
        try:
            response = requests.get(url)
            json_obj = response.json()
            for obj in json_obj:
               	t1 = threading.Thread(target=self.cal_square, args=(obj,channel_id,))
               	t1.start()
               	t1.join()
            print("Done API")
            return url
        except ValueError as error:
            print(error)
            pass
    def main_crawl_data(self):
        i = 0
        channel_id = 4
        while True:
            url_crawl = "https://www.foxnews.com/api/article-search?searchBy=tags&values=fox-news%2Ffood-drink,fox-news%2Fhouse-and-home,fox-news%2Fauto,fox-news%2Ffitness-and-wellbeing,fox-news%2Ftravel,fox-news%2Fstyle-and-beauty,fox-news%2Fgreat-outdoors,fox-news%2Freal-estate,fox-news%2Flifestyle,fox-news%2Ftravel%2Fgeneral%2Fairlines,fox-news%2Ftravel%2Fgeneral%2Fairports&excludeBy=tags&excludeValues=&size=30&from="+str(i*30)+"&mediaTags=health%7Cnutrition_fitness%7Cfitness,lifestyle%7Creal_estate,travel%7Cgeneral%7Cairlines&isSection=true"
            page = self.crawl_data(url_crawl,channel_id)
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
                    print(date_new)
                    print('Finish')
                    return
            if page == 0:
                print('Finish')
                return
            if i ==  300:
                print('Finish')
                return
            i +=1
            print("Success")