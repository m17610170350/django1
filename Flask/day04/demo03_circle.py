#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
在实际开发中不可能所有的代码都写在同一个文件,所以必须要进行模块化开发
但是在分模块开发的时候容易循环导入包问题:
解决办法:
1. 先在一个文件中定义视图函数, 再到另外一个文件中装饰
    缺点: 维护起来比较麻烦,所有的装饰都写在了同一个应用程序中
2. 使用蓝图
"""""

from flask import Flask
from user import get_user_info
import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

@app.route("/get_order_info")
def get_order_info():
    return "get_order_info"

app.route("/get_user_info")(get_user_info)

@app.route("/")
def index():

    return "index"

if __name__ == '__main__':
    print (app.url_map)
    app.run(debug=True)