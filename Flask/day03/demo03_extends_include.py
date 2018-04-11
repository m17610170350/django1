#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
jinja2中提供了一些模板的使用,支持继承和包含
模板的定义格式:
    {% block 名字 %}

    {% endblock%}

继承特点: 共性抽取,代码复用
格式:
    {% extends '模板文件名' %}
    {% block 父类某个模板名字 %} 覆盖了父类中的内容
    {{ super() }} 可以保留父类的内容

包含特点: 对于不会发生改变的文件使用包含
    {% include '模板文件名' %}
    {% include '模板文件名' ignore missing%} 如果模板不存在,也不会报错
"""""

from flask import Flask, render_template

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


@app.route("/")
def extends():

    return render_template("file_extends.html")

@app.route("/include")
def include():

    return render_template("file_include.html")

if __name__ == '__main__':
    app.run(debug=True)
