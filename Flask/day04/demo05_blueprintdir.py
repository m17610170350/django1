#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
以目录的形式使用蓝图
使用流程:
1. 创建包(有__init__文件)
2. 在包的init文件中创建蓝图对象
3. 在该包下的模块中编写视图函数,使用蓝图对象装饰
4. 将蓝图对象导入到应用程序app中进行注册

"""""

from flask import Flask
from cart import  cart


app = Flask(__name__)


#注册蓝图兑现到app中
app.register_blueprint(cart,url_prefix = "/cart")


@app.route('/')
def index():

    return "helloworld"

if __name__ == "__main__":
    print app.url_map
    app.run(debug=True)