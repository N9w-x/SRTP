#encoding=utf-8
import pymysql

connection = 0;
cursor = 0;

#登陆数据库,三个参数分别为用户名，密码，想要操作的数据库

def login(user,pw,db):
    username  = user
    password = pw
    database = db
    try:
        global connection
        connection = pymysql.connect(
            host = "localhost",
            user = username,
            password = password,
            db = database,
            charset = "utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        global cursor;
        cursor = connection.cursor()
        print("登录成功")
    except pymysql.Error as e:
        print(e)
        print("登录失败")

def logout():
    connection.close()
    print("登出数据库")

# db为字符串，指定database的名字
def change_database(db):
    sql = "USE "+db
    try:
        cursor.execute(sql)
        print("切换到"+db)
    except pymysql.Error as e:
        print("不存在该数据库")

def create_db(name):
    sql = "CREATE DATABASE IF NOT EXISTS " + name
    cursor.execute(sql)
    cursor.execute("USE "+name)
    sql="""CREATE table 
        IF NOT EXISTS webinfo(
            year INT,
            month INT,
            day INT,
            hour INT,
            min INT,
            sec INT,
            title VARCHAR(100) ,
            source VARCHAR(50) NULL,
            author VARCHAR(50)NULL,
            `text` text,
            PRIMARY KEY  (title)
        )
        """
    cursor.execute(sql)
    print('数据库'+name+"创建成功")
# name是当前数据库的名字
def insert(y,m,d,h,min,sec,title,source,author,text,name):
    sql = "USE " + name 
    try:
        cursor.execute(sql)
    except pymysql.Error as e:
        print(e)
        print("不存在该数据库")
    try:
        cursor.execute(
            "REPLACE INTO webinfo VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [y,m,d,h,min,sec,title,source,author,text,]
        )
        connection.commit()
        print("插入数据成功")
    except pymysql.Error as e:
        print("插入数据失败")
        connection.rollback()


