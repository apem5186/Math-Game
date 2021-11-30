from pymysql import cursors
import pymysql

# conn = pymysql.connect(
#     host="localhost",
#     port=3306,
#     user="root",
#     password="tls135712!",
#     db="math_game",
#     charset="utf8mb4",
# )
# cursor = conn.cursors()

# sql = "insert into user(userName, userPass) values (%s, %s)"
# val = ("hello", int(1234))

# cursor.execute(sql, val)
# conn.commit

# print(cursor.rowcount, "record inserted")
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
            print(id, passWord)
            print("success")
    except Exception as e:
        print(e)



# try:
#     with conn.cursor() as curs:
#         sql = "select userName from user"
#         curs.execute(sql)
#         rs = curs.fetchall()
#         for row in rs:
#             print(row)
# finally:
#     conn.close()
