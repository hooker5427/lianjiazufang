import pymysql

connect = pymysql.connect('47.115.21.129', 'root', '111111')
cursor = connect.cursor()
try:
    cursor.execute('create database lianjia charset="utf8";')
    print('创建数据库成功Daatabase created')
except:
    print('Database lianjia exists!')
connect.select_db('lianjia')


sql = """CREATE TABLE lianjia_spider (
         title VARCHAR(200),
         link VARCHAR(200),
         location VARCHAR(200),
         rent VARCHAR(200),
         apartment_layout VARCHAR(200),
         area VARCHAR(200),
         orientation VARCHAR(200),
         longitude VARCHAR(200),
         latitude VARCHAR(200),
         publish_time VARCHAR(200),
         unit_price FLOAT,
         floor VARCHAR(200),
         created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

cursor.execute(sql)
connect.commit()
connect.close()