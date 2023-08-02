from flask import Flask, jsonify, request
import pymysql
import configparser
from flask_cors import CORS

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取数据库连接信息
db_host = config.get('database', 'host')
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')
db_name = config.get('database', 'database')

app = Flask(__name__)
CORS(app)

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


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'name' not in data or 'password' not in data:
        return jsonify({'message': 'Missing name or password'}), 400

    name = data['name']
    password = data['password']

    with conn.cursor() as cursor:
        query = "SELECT * FROM user_info WHERE name = %s AND password = %s"
        cursor.execute(query, (name, password))
        user = cursor.fetchone()

    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
