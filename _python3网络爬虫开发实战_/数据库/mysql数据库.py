# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:

import pymysql
db = pymysql.connect(host = 'localhost', user = 'root', password = '', port = 3306)
cursor = db.cursor()#操作游标
cursor.execute('SELECT VERSION()')#获取版本信息
data = cursor.fetchone()#找到版本信息
print('Datebase version:',data)

#第一步：创建数据库
'''创建数据库'''
cursor.execute("CREATE DATABASE news DEFAULT CHARACTER SET utf8")#创建数据库
db.close()
'''第二次创建报错：pymysql.err.ProgrammingError: (1007, "Can't create database 'spiders'; database exists")'''


#第二步：创建表
db = pymysql.connect(host = 'localhost', user = 'root', password = '', port = 3306,
                     db='spider')#db='spiders'必须先创建
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(225) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY(id))'
cursor.execute(sql)
#db.close()
'''问题：pymysql.err.InternalError: (1049, "Unknown database 'spiders'")，似乎是之前的创库没有创，之后可能不用了'''
'''db.close()后需要重新构建db=.......'''

#第三步数据插入
id = '2012010203'
name = 'bob'
age = 20
cursor = db.cursor()
sql = 'INSERT INTO students(id,name,age) values(%s, %s, %s)'
try:
    cursor.execute(sql, (id, name, age))
    db.commit()
except:
    db.rollback()
#db.close()

#读取数据
sql = 'SELECT * FROM students WHERE age >= 20'
res = 'SELECT * FROM students'#即为查看所有
try:
    cursor.execute(sql)
    print('Count: ',cursor.rowcount)
except:
    print('Error')
#db.close()



