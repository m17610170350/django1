#!/usr/bin/ python3
# -*-coding:utf-8-*-
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# CSRFProtect只做验证工作，cookie中的 csrf_token 和表单中的 csrf_token 需要我们自己实现
from flask_wtf import CSRFProtect
from flask_session import Session
from config import config_dict

import sys

from utils.commons import RegexConverter

reload(sys)
sys.setdefaultencoding('utf8')

# 创建数据库对象
db = SQLAlchemy()
"""# 全局可用的redis
redis_store = None
# 包含请求体的请求都需要开启CSRF
csrf = CSRFProtect()
# 开启Session
Session()"""


# 工厂方法, 根据[配置信息,返回对应的app对象
def create_app(config_name):


    # 创建应用程序对象
    app = Flask(__name__)

    # 通过配置名先获取到配置类
    config = config_dict.get(config_name)
    # print(config)
    # 配置
    app.config.from_object(config)

    # 创建日志记录文件
    log_file(config.DEBUG_LEVEL)


    # 初始化数据库
    db.init_app(app)

    # 设置 redis
    global redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    # 开启Session
    Session(app)

    # 开启csrf保护
    CSRFProtect(app)

    # 添加一个re转换器到转换器列表中
    app.url_map.converters["re"] = RegexConverter

    # 注册蓝图
    from api_1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1.0')

    #注册静态文件蓝图
    from web_html import html
    app.register_blueprint(html)

    # print(app.url_map)

    return app


def log_file(config_level):
    # 设置日志的记录等级
    logging.basicConfig(level=config_level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)