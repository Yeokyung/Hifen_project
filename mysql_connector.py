# reference : https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html
# 방법 1 : 데이터만 추출하고 싶을때

# pip install mysql-connector-python (상위 버전)
# pip install mysql.connector (하위 버전)

import mysql.connector

mydb = mysql.connector.connect(
    host="~~~amazon.com",
    port='3306',
    user="username",
    passwd="userpw",
    database="hifen"  # database 이름
)

cur = mydb.cursor()
cur.execute("select * from hifen.utuber_info")
myresult = cur.fetchmany(2)

for x in myresult:
    print(x)

import pandas as pd

pd.DataFrame(myresult)

# 방법 2 : 칼럼명이랑 같이 추출
# pip install PyMySQL

import pymysql

mydb = pymysql.connect(
    user='username',
    passwd='userpw',
    host='~~~amazon.com',
    db='hifen'
)

cur = mydb.cursor(pymysql.cursors.DictCursor)
cur.execute("select * from utuber_info")
myresult = cur.fetchmany(10)
# fetchall() : 데이터 모두 호출 / fetchone() : 데이터 한개만 호출하고 싶을때 , fetchmany(n) : 데이터 n개 호출

for x in myresult:
    print(x)

import pandas as pd
pd.DataFrame(myresult)