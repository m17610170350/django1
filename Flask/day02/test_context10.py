#!/usr/bin/ python3
# -*-coding:utf-8-*-
import sys
import redis
from flask import Flask
from flask import request
from flask_session import Session


reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


class Content:
    SECRET_KEY = "helloworld"
    SESSION_TYPE = "redis"  # 指明保存到redis中
    SESSION_USE_SIGNER = False  # 让cookie中的session_id被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host="127.0.0.1", port=6379)  # 使用的redis实例
    PERMANENT_SESSION_LIFETIME = 86400


app.config.from_object(Content)
Session(app)


@app.route("/")
def request_context():
    name = request.args.get("name", "haha")
    return name


if __name__ == '__main__':
    app.run(debug=True)
