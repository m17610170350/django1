#!/usr/bin/ python3
# -*-coding:utf-8-*-
# from __future__ import print_function
from flask import Flask

app = Flask(__name__)


@app.route("/<path:number>")
def index(number):
    str = "啦啦啦"

    print type(str)
    print type(u'number')

    return "有你口%s"% number


if __name__ == '__main__':
    app.run()
