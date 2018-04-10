#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
cookie: 用来记录浏览器和服务器之间交互的数据信息,保存在客户端(浏览器中).
设置cookie的格式:
    resp = make_response()
    resp.set_cookie(key,value,maxAge) #maxAge设置cookie的有效期,单位秒
    return resp

获取cookie的方式
    value =  request.cookies.get(key)
"""""

from flask import Flask
from flask import make_response
from flask import request

app = Flask(__name__)

@app.route("/set_cookie")
def set_cookie():
    resp = make_response("hello world")
    resp.set_cookie("name", "zhang_san")
    resp.set_cookie("age", "18", 10)
    return resp

@app.route("/get_cookie")
def get_cookie():
    name = request.cookies.get("name")
    age = request.cookies.get("age")
    return "get_cookie name is %s, age is %s"%(name,age)
    
    
if __name__ == '__main__':
    app.run(debug=True)