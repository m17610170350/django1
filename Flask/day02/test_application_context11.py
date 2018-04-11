#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
应用上下文:
current_app: 当我们在其他的文件中需要使用到app应用对象内容的时候,可以通过current_app来进行代替,相当于app对象的一个提示
             在项目中进行多文件开发的时候使用
"""""

from flask import Flask, current_app

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


@app.route("/index1")
def index1():
    return "index1"

@app.route('/index2')
def index2():
    return "index2"

@app.route('/index3')
def index3():

    print current_app.url_map
    print "1212"
    return "index3"


if __name__ == '__main__':
    print (app.url_map)
    app.run(debug=True)
