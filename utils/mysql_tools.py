import pymysql


# 连接到数据库
def connect_mysql():
    conn = pymysql.connect(host='localhost', user='root', password='123', database='tcm', charset='utf8')
    cur = conn.cursor()
    return cur, conn


# 得到数据库数据
def get_mysql_data(sql):
    cur, conn = connect_mysql()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# 得到数据库数据
def get_mysql_data_1(sql, text):
    cur, conn = connect_mysql()
    cur.execute(sql, text)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
