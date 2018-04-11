#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
在使用flask程序向浏览器数据的使用可以使用jinjia2提供的模板渲染页面
默认的模板文件资源在: templates文件夹中

使用步骤:
    render_template("模板页面")

"""""

from flask import Flask, render_template

import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

@app.route("/")
def index():

    return render_template("file01.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)