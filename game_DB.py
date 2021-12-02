from types import new_class
import numpy
from pygame.sndarray import array
from pymysql import NULL, cursors
import pymysql
import json
import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
def con():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="tls135712!",
        db="math_game",
        charset="utf8",
        port=3306,
        autocommit=True
    )
    return conn

def id_check(id):
        with con().cursor() as curs:
            sql = "select * from user where userName = %s"
            if curs.execute(sql, (id)):
                return True

def pass_check(passWord):
        with con().cursor() as curs:
            sql = "select * from user where userPass = %s"
            if curs.execute(sql, (passWord)):
                return True

def join_id_check(id, passWord):
    try:
        with con().cursor() as curs:
            sql = "insert into user(userName, userPass) values(%s, %s)"
            curs.execute(sql, (id, passWord))
            sql = "insert into userpoint(userName) values(%s)"
            curs.execute(sql, id)
            sql = """update userpoint set point = '{"points": []}'"""
            curs.execute(sql)
            print(id, passWord)
            print("success")
    except Exception as e:
        print(e)

def insert_point(id, points):
    try:
        with con().cursor() as curs:
            sql = """update userpoint set point = JSON_ARRAY_APPEND(point, '$.points', %s) where userName = %s"""
            curs.execute(sql, (points, id))
    except Exception as e:
        print(e)

def get_point(id):
    try:
        with con().cursor(pymysql.cursors.DictCursor) as curs:
            sql = """select point from userpoint where userName = %s"""
            curs.execute(sql, (id))
            result = curs.fetchone()
            json_data = json.dumps(result)
            json_data = json.loads(json_data)
            json_data = json_data['point']
            json_data = json.loads(json_data)
            json_data = json_data['points']
            return json_data
    except Exception as e:
        print(e)
n = len(get_point("hi"))
nn = range(1, n+1)
print(nn)
print(n)
get_point("hi")
plt.plot(nn, get_point("hi"))
plt.show()