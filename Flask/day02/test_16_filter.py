#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
在使用模板的时候,已经提供了相应的过滤方式(函数),常见的过滤方式有:
1. 字符串的过滤
    格式: {{ 字符串 | 过滤方式 }}
    过滤方式:
        capatilize
        titile
        reverser
        .....


2. 列表过滤
     格式: {{ 列表 | 过滤方式 }}
    过滤方式:
        sort
        ....

"""""

from flask import Flask,render_template

import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

@app.route("/")
def index():
    list = [x for x in range(1,10,2)]
    return render_template("file02.html", list=list)

if __name__ == '__main__':
    app.run(debug=True)