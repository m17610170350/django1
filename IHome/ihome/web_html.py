#!/usr/bin/ python3
# -*-coding:utf-8-*-
from flask import Blueprint
# 创建蓝图对象
from flask import current_app
from flask.ext.wtf.csrf import generate_csrf

html = Blueprint("web_html", __name__)

@html.route("/<re(r'.*'):file_name>")
def get_html_page(file_name):

    # 判断是否是访问的根路径,如果是,就去访问index.html
    if not file_name:
        file_name = "index.html"
    # 拼接访问路径html/
    if file_name != "favicon.ico":
        file_name = "html/" + file_name

    response = current_app.send_static_file(file_name)


    #给cookie中设置csrf_token
    token = generate_csrf()
    response.set_cookie("csrf_token",token)

    return response