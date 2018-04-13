#!/usr/bin/ python3
# -*-coding:utf-8-*-
from flask import Flask, jsonify

import sys

from flask import request

reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

#-2 表示用户名或者密码为空
#0 表示登录成功
#-1 表示用户名或者密码错误

@app.route("/login", methods=["POST", "GET"])
def login():

    # 获取参数
    username = request.form.get("username")
    password = request.form.get("password")
    print username, password
    # 校验,判断
    if not all([username, password]):
        resp_dict = {
            "errcode":-2,
            "message":"username or password is none"
        }

        return jsonify(resp_dict)

    #3.验证用户名密码的正确性
    if username == "admin" and password == "123":
        resp_dict = {
            "errcode":0,
            "message":"login success"
        }
        return jsonify(resp_dict)

    else:
        resp_dict = {
            "errcode":-1,
            "message": "usrename or password is wrong"
        }
        return jsonify(resp_dict)

if __name__ == '__main__':
    app.run(debug=True)