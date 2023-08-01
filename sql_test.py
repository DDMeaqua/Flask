from pymysql import Connection
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取数据库连接信息
db_host = config.get('database', 'host')
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')
db_name = config.get('database', 'database')

try:
    # 获取mysql链接对象
    conn = Connection(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        autocommit=True,
    )
    print("连接成功")
    # 打印mysql信息
    print(conn.get_server_info())
except Connection as err:
    print("寄")
    exit()
# 关闭链接
conn.close()