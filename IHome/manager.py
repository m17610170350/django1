#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
第一步:
1.数据库配置,数据库迁移等
2.配置redis
3.配置session
4.csrf保护机制
5.日志信息等

第二步:
项目分层

第三步:
视图函数,业务逻辑编写

设置模板文件:
file --settings-->edit_keymap -->live template -->flask -->点击添加

注意点:
1. csrf机制会对POST,PUT,DELETE,PATCH进行保护
2. flask_session用来指定session的存储位置
"""""
from flask.ext.migrate import MigrateCommand, Migrate
from flask_script import Manager
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# CSRFProtect只做验证工作，cookie中的 csrf_token 和表单中的 csrf_token 需要我们自己实现
from flask_wtf import CSRFProtect
from flask_session import Session

import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)


# 先在当前类中定义配置的类，并从中加载配置
class BaseConfig:

    SECRET_KEY = "laizonghuiyilu"
    # 配置app的配置类
    DEBUG = True
    # 导入数据库扩展，并在配置中填写相关配置

    # mysql 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@localhost:3306/ihome_flask"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 创建redis存储对象，并在配置中填写相关配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 利用flask - session扩展，将session数据保存到Redis中
    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒



app.config.from_object(BaseConfig)

# 包含请求体的请求都需要开启CSRF
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT)
Session(app)


manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

@app.route("/index")
def index():

    return "index"

if __name__ == '__main__':
    manager.run()