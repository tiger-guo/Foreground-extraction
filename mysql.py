'''fetchone'''
import pymysql


def loginByUserAndPW(name, password):
    #打开数据库连接
    conn=pymysql.connect('localhost','root','admin')
    conn.select_db('testdb')
    #获取游标
    cur=conn.cursor()
    sql = "select * from user where name = %s "
    cur.execute(sql, name)
    while 1:
        res=cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()
        if res[2] == password:
            return True
        else:
            return False

def loginByUserName(name):
    #打开数据库连接
    conn=pymysql.connect('localhost','root','admin')
    conn.select_db('testdb')
    #获取游标
    cur=conn.cursor()
    sql = "select * from user where name = %s "
    cur.execute(sql, name)
    res=cur.fetchone()
    cur.close()
    conn.commit()
    conn.close()
    if res == None:
        return False
    else:
        return True


def addUser(name, password):
    conn = pymysql.connect('localhost', 'root', 'admin')
    conn.select_db('testdb')

    cur = conn.cursor()  # 获取游标

    # 另一种插入数据的方式，通过字符串传入值
    sql = "insert into user(name, password) values(%s, %s)"
    cur.execute(sql, (name, password))

    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')

