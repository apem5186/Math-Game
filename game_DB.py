from types import new_class
import numpy
from pygame.sndarray import array
from pymysql import NULL, cursors
import pymysql
import json
import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

import matplotlib.pyplot as plt


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
# def show_record():
#     fig = plt.figure(figsize=[4, 4], # Inches
#                     dpi=150,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
#                     )

#     canvas = agg.FigureCanvasAgg(fig)
#     canvas.draw()
#     renderer = canvas.get_renderer()
#     raw_data = renderer.tostring_rgb()
#     size = canvas.get_width_height()
#     return raw_data, size

    

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
            sql = """update userpoint set point = '{"points": []}' where userName = %s"""
            curs.execute(sql, id)
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

def get_total():
    try:
        with con().cursor() as curs:
            sql = """select total from userpoint"""
            curs.execute(sql)
            result = curs.fetchall()
            return result
    except Exception as e:
        print(e)

def get_name(total):
    try:
        with con().cursor() as curs:
            sql = """select userName from userpoint where total = %s"""
            curs.execute(sql, (total))
            result = curs.fetchone()
            return result
    except Exception as e:
        print(e)

def insert_total(score, id):
    try:
        with con().cursor() as curs:
            sql = """update userpoint set total = %s where userName = %s"""
            curs.execute(sql, (score, id))
    except Exception as e:
        print(e)
point = get_total()
points = []
name = []
for i in point:
    points += list(i)
    name += list(get_name(i))

# print(get_name(35)[0])
# print(points)
# print(name)
