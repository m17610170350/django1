#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
reqeust是和请求对象相关的,通过该对象可以获取到请求的数据
    比如:
        request.data : 获取到请求数据(post),字符串表示形式
        request.url  : 获取到请求的url
        request.method: 请求方式
        request.form : 获取到表单数据
        .....

"""""

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    data = request.data
    url = request.url
    method = request.method
    form = request.form
    print (data, url, method, form)
    return "index"

if __name__ == '__main__':
    app.run(debug=True)