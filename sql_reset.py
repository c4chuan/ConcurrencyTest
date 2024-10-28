import pymysql

def sql_reset():
    # 连接数据库
    db = pymysql.connect(host='47.108.135.99', port=3306, user='myuser', passwd='ShuWen1234..', db='data',
                         charset='utf8')
    cursor = db.cursor()
    print("连接数据库成功")

    table_name = ['GAD-7', 'instant_info', 'PHQ-9', 'result', 'student_info', 'topic']
    # 清空表
    for i in range(len(table_name)):
        sql = "truncate table " + '`' + table_name[i] + '`'
        cursor.execute(sql)
        print(table_name[i] + "表清空成功")
    return 200