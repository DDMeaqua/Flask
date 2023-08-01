from flask import Flask, jsonify
import pymysql
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取数据库连接信息
db_host = config.get('database', 'host')
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')
db_name = config.get('database', 'database')

app = Flask(__name__)

# 创建数据库连接
conn = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    autocommit=True,
)


@app.route('/', methods=['GET'])
def get_user():
    with conn.cursor() as cursor:
        query = "SELECT name,phone FROM user_info"
        cursor.execute(query)
        data = cursor.fetchall()

    return jsonify(data)


@app.route('/api/user', methods=['GET'])
def get_data():
    with conn.cursor() as cursor:
        query = "SELECT * FROM test"  # 替换为你的表名
        cursor.execute(query)
        data = cursor.fetchall()

    # 将数据转换成 JSON 格式并返回
    return jsonify(data)


@app.route('/api/info', methods=['GET'])
def get_info():
    with conn.cursor() as cursor:
        query = """ 
        SELECT user_info.name, user_info.phone, user_info.email, test.city
        FROM user_info
        INNER JOIN test ON user_info.name = test.name;
        """
        cursor.execute(query)
        data = cursor.fetchall()

    # 将数据转换成 JSON 格式并返回
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
