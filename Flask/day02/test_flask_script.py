#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
往往在实际的开发中,有可能改变服务器运行的ip和端口号,需要找到指定的代码去修改ip和端口
有没有一种方式,不改变源代码的情况下就能, 指定服务七的端口和ip

flask_script: 在运行程序的时候可以指定ip,和端口

使用步骤:
1. 导入模块
2. 创建Manager管理对象,关联app应用程序
3. 使用manager进行启动: manager.run()
启动方式: python xxxx.py runserver -h ip地址 -p 端口号

"""""

from flask import Flask

import sys

from flask.ext.script import Manager

reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
manager = Manager(app)

@app.route("/")
def index():

    return "index"

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()