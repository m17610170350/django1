#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
服务器给浏览器返回数据的时候格式:
元祖格式:
1. 直接返回响应体,  2. 直接返回响应体+状态码, 3.直接返回响应体+状态码+响应头

2. 返回response对象
    resp = make_response("响应体","状态码","响应头")
    return resp

    resp = make_response("响应体")
    resp.status = "666 BigError"
    resp.headers["Content-Type"] = "application/json"
    return resp

"""""

from flask import Flask
from flask import make_response

app = Flask(__name__)

@app.route("/")
def index():
    # 1.直接返回响应体, 2.直接返回响应体 + 状态码, 3.直接返回响应体 + 状态码 + 响应头
    # resp = make_response("hello world", "233 BigError", {"Content-Type":"application/json","name":"zhangsan"})
    # return resp

    #2.分开设置然后返回
    resp = make_response("HelloWorld")
    resp.status = "232 big"
    resp.headers["Content-Type"] = "application/json"
    resp.headers["name"] = "lisi"
    return resp

if __name__ == '__main__':
    app.run(debug=True)