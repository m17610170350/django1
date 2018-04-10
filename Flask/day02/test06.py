#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
在执行一个视图函数的时候,如何自动跳转到另外一个视图函数中运行?
可以使用重定向(redirect)
使用格式: redirect("路由的路径")

重定向特点: 两次请求
转发: 一次请求
"""""

from flask import Flask
from flask import redirect

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/index2")


@app.route("/index2")
def index2():
    return "my name is index2"


if __name__ == '__main__':
    app.run(debug=True)
