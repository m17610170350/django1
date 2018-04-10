#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
abort(代号): 在程序运行的过程当中,一旦执行,主动跑出异常代号, 和raise 异常对象 相似

@app.errorhandler(代号/异常对象): 捕捉异常代号,或者是异常对象,和abort配合使用,用来自定义友好提示

"""""

from flask import Flask
from flask import abort

app = Flask(__name__)


@app.route("/<int:number>")
def index(number):
    if number == 1:
        abort(403)
        # 1/0
        # raise Exception("大异常")
    elif number == 2:
        abort(404)
    else:
        return "youtube"


# @app.errorhandler(Exception)
# def not_found_exception(e):
#     return "好大异常， %s" % e

@app.errorhandler(ZeroDivisionError)
def not_found_zero(e):
    return "不能除0"

@app.errorhandler(403)
def not_found_403(e):
    return "你没有权限访问"

@app.errorhandler(404)
def not_found_403(e):
    return "找不到指定页面"

if __name__ == '__main__':
    app.run(debug=True)
