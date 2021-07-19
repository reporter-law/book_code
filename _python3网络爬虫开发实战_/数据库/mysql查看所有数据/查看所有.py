"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import pymysql

def get_tables_from_db():
    tables = []
    # 连接参数配置
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
    }
    # 连接数据库
    con = pymysql.connect(**config)
    # 创建游标
    cursor = con.cursor()
    # 查询语句
    # 查询指定的数据库下有多少数据表
    sql = 'select TABLE_NAME, table_type, engine from information_schema.tables where table_schema="wenshu"'

    try:
        # 执行查询语句
        cursor.execute(sql)
        # 取得所有结果
        results = cursor.fetchall()
        # 打印数据表个数
        print(len(results))
        # 打印数据表名，数据表类型，及存储引擎类型
        print("table_name", "table_type", "engine")
        for row in results:
            name = row[0]
            type = row[1]
            engine = row[2]
            tables.append(name)
            print(name, type, engine)
    except Exception as e:
        raise e
    finally:
        con.close()
    return tables

tables = get_tables_from_db()
