#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
蓝图: 就是用来模块化开发的
使用流程:
1. 创建蓝图对象
2. 使用蓝图装饰视图函数
3. 将蓝图对象注册app中

蓝图理解: 蓝图实际上就是一个列表, 在注册时候,会将蓝图中的所有视图函数的映射关系, 添加到app的url_map中

"""""
from flask import Flask
from product import product
import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

#将蓝图对象注册到应用程序app中
app.register_blueprint(product)


@app.route("/")
def i():

    return "hello world"

if __name__ == '__main__':
    print (app.url_map)
    app.run(debug=True)