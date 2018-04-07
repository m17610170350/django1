#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
如果通过一个视图函数找到,对应的路由路径?
使用url_for方法
    使用格式: url_for("视图函数名称")
    在flask模块中

练习:
找班长借钱, 班没有,让找副班长借钱.

"""""
from flask import Flask, url_for

app = Flask(__name__)
@app.route("/")
def index():

    return "班长点草<a href='%s'>副班长</a>"% url_for("index2")


@app.route('/index')
def index2():

    return "laiba"

if __name__ == '__main__':
    app.run()