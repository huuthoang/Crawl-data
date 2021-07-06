import mysql.connector
from random import randint
from datetime import datetime
import names
import random

first_names = {"Nguyễn", "Trần", "Lê", "Hứa", "Hồ", "Mạc", "Tần", "Phạm", "Hoàng", "Phan", "Huỳnh", "Vũ", "Võ ", "Đặng"}
middle_names = {"Thị", "Ngọc", "Anh", "Hoàng", "Thảo", "Toàn", "Thành", "Phát", "Tâm","Tính","Thiện","Linh","Điền"}
last_names = {"Tuấn", "Ngọc", "Anh", "Hoàng", "Thảo", "Toàn", "Thành", "Phát", "Tâm","Tính","Thiện","Linh","Điền"}

now = datetime.now()
date = now.strftime("%Y/%m/%d %H:%M:%S")
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="123456",
  database="bosscake"
)

mycursor = mydb.cursor()
users = """INSERT INTO users 
        (id,
         name,
         email,
         password,
         confirmed,
         gender,
         is_client,
         created_at,
         updated_at) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
user_summary = """INSERT INTO user_summary 
        (user_id,
         duration_seconds,
         total_score,
         level,
         star,
         created_at,
         updated_at) 
        VALUES (%s,%s,%s,%s,%s,%s,%s)"""
def Name(first_names,middle, last_names):
    first = random.sample(first_names, 1)[0]
    middle = random.sample(first_names - {first}, 1)[0]
    last = random.sample(last_names - {first}, 1)[0]
    return (first + " "+ middle + " " + last)
def CheckLevel(level):
    n = 1
    score = randint(level*n, level*50)
    return score
OUT=[]
for i in range(1000):
    id = i + 2
    if i%11 == 0:
        name = names.get_full_name()
    else:
        name=Name(first_names, middle_names,last_names)
    email = names.get_full_name()+"@gmail.com"
    password = "$2y$10$Ru43uhffLPfSk8M1CsappeTUAcY0EYRANwADm5jus79nx1bVZZwWW"
    if i%2 == 0:
        gender = "F"
    else:
        gender = "M"
    data_user = (id,name,email,password,0,gender,0,date,date)
    mycursor.execute(users, data_user)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
for i in range(1000):
     user_id = i + 2
     level = randint(1, 10)
     total_score = CheckLevel(level)
     data_user_summary = (user_id,randint(5, 100),total_score,level,randint(10, 1000),date,date)
     mycursor.execute(user_summary, data_user_summary)
     mydb.commit()
     print(mycursor.rowcount, "record inserted.")

