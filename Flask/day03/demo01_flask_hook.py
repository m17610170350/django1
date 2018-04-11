#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
flask中提供一种机制,叫请求钩子: 往往在实际开发中,不同的业务需要使用不同的视图函数进行处理,比如在程序开始
运行的时候,有一些初始化的操作,或者一些扫尾的工作要做.

常见的请求钩子有以下四种:
1. before_first_request, 只有在第一次请求的时候才会执行
2. before_request, 每次请求的时候都会执行,
3. after_request,每次请求结束后执行
4. teardown_request, 请求结束后执行,如果有异常传递到修饰的函数中

"""""

from flask import Flask, request

import sys


reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

@app.before_first_request
def before_first_request():
    print("只有在第一次请求的时候才会执行,初始化,链接数据库,文件创建")

@app.before_request
def before_request():
    print ("每次请求的时候都会执行, 参数校验,统计")
    print request.url
    # if 校验

@app.after_request
def after_request(response):
    print ("每次请求结束后执行,统一设置服务端和客户端的一些数据交互格式")
    response.headers["Content-Type"] = "application/json"
    return response

@app.teardown_request
def teardown_request(e):
    print ("请求结束后执行, 会如果服务器发生了异常,会传递一个参数过来")
    print e
@app.route("/")
def index():

    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)