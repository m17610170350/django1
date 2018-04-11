#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
在jinja2中提供了一些常见的变量,不需要从flask程序中传递过去就可以使用
常见特殊变量:
request: 请求对象
g: 应用上下文对象
config: 应用程序的配置对象
url_for(): 反解析方法
get_flashed_messages(): 消息队列方法, 可以获取到设置在flash()方法中的内容,
依赖了session所以需要设置SECRET_KEY

"""""
from flask import Flask,render_template,g,flash

import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
app.config["SECRET_KEY"] = "khfdiuhnlkawedh"

@app.route("/")
def index():
    g.username = "zhaangsan"

    flash("错误信息1")
    flash("错误信息2")
    flash("错误信息3")
    flash("错误信息4")

    return render_template("file_variable.html")

@app.route("/test")
def test():
    pass


if __name__ == '__main__':
    app.run(debug=True)