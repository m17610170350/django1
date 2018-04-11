#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
g: 用来存储用户的数据库,登录信息,每次请求的时候都会创建一个新的对象
   配合装饰器

   g对象,配合装饰器,验证用户是否有登录
"""""
from functools import wraps
from flask import Flask,g
from flask import session

app = Flask(__name__)
app.config["SECRET_KEY"] = "helo"

# 使用g对象编写装饰器
def login_required(view_func):
    """检验用户的登录状态"""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        username = session.get("username")
        if username is not None:
            # 表示用户已经登录
            # 使用g对象保存user_id，在视图函数中可以直接使用
            g.username = username
            return view_func(*args, **kwargs)
        else:
            # 用户未登录
           return "helloworld"
    return wrapper

@app.route('/')
def login():
    session["username"] = "zhangsan"
    return "已经登录"

@app.route('/get_info')
@login_required
def get_info():
    return "获取了网页详细信息%s"%g.username


@app.route('/get_order')
@login_required
def get_order():
    return "获取订单信息"

if __name__ == "__main__":
    print app.url_map
    app.run(debug=True)