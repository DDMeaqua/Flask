import configparser
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取数据库连接信息
db_host = config.get('database', 'host')
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')
db_name = config.get('database', 'database')

# Mysql所在的服务器地址
HOSTNAME = db_host
# 端口号
PORT = 3306
# 数据库用户名
USERNAME = db_user
# 数据库密码
PASSWORD = db_password
# 数据库名称
DATABASE = db_name

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

# 在app.config中设置好链接数据库的信息
# 然后使用sqlalchemy(app)创建一个db对象
# SQLAlchemy会自动的从app.config中读取链接数据库的配置信息
db = SQLAlchemy(app)

with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar, null=0
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # articles = db.relationship("Article", back_populates="author")


# user = User(username="法外狂徒张三", password="123456")
# sql: insert into user(username,password) values('法外狂徒张三','123456')

class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # backref:会自动给User模型添加一个articles的属性 用来获取文章列表
    author = db.relationship("User", backref="articles")
    # author = db.relationship("User", back_populates="articles")


# article = Article(title="xxx小说", content="Flaskxxx")

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/add')
def add_user():
    # 创建ORM对象
    user = User(username="法外狂徒张三", password="123456")
    # 将ORM对象添加到db.session中
    db.session.add(user)
    # 提交到数据库
    db.session.commit()
    return 'add user success'


@app.route('/user/query')
def query_user():
    # get查找
    user = User.query.get(1)
    print(f"{user.id}:{user.username}---{user.password}")
    # filter_by查找
    users = User.query.filter_by(username="法外狂徒张三")
    for user in users:
        print(user.username)
    return "查询成功"


@app.route("/user/update")
def update_user():
    user = User.query.filter_by(username="法外狂徒张三").first()
    user.password = "222222"
    db.session.commit()
    return "数据修改成功"


@app.route("/user/delete")
def delete_user():
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "数据删除成功"


@app.route("/article/add")
def art_add():
    article1 = Article(title="某小说", content="清晨醒来第一句话：")
    article1.author = User.query.get(2)

    article2 = Article(title="x某小说", content="清晨一句话：")
    article2.author = User.query.get(2)

    db.session.add_all([article1, article2])
    db.session.commit()

    return "小说添加成功"


@app.route("/article/query")
def art_query():
    user = User.query.get(2)
    for article in user.articles:
        print(article.title)
    return "文章查找成功"


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    app.run(debug=True, host='0.0.0.0', port=8080)
