#!/usr/bin/ python3
# -*-coding:utf-8-*-


from flask import Flask

app = Flask(__name__)

# 多个路由装饰一个视图函数，都可以访问到函数
@app.route("/")
@app.route('/index1')
def index1():

    return "index1"


# 一个路由装饰多个函数，会先访问先被装饰的
@app.route("/index2")
def index2():
    return "index2"


@app.route("/index2")
def index22():
    return "index22"

if __name__ == '__main__':
    print app.url_map
    app.run()