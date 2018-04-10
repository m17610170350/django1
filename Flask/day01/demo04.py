#!/usr/bin/ python3
# -*-coding:utf-8-*-

from flask import Flask

app = Flask(__name__)

# 路由后面添加methods参数，指定请求的方法
@app.route("/", methods=["POST"])
def index():

    return "index"


if __name__ == '__main__':
    app.run()