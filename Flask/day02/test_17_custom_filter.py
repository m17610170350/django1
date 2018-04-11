#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
当jinjia2提供的默认模板满足不了我们开发需求的时候,可以自定义模板,有两种方式:
方式一:
1. 定义视图函数
2. 使用app.add_template_filter(函数名字, "模板名字")


方式二:
直接定义视图函数使用@app.template_filter("模板名字")

"""""

from flask import Flask
from flask import render_template

app = Flask(__name__)

# 方式一:
# 1. 定义视图函数
def get_new_list(list):
    new_list = []
    for a in list:
        if a %2 == 0:
            new_list.append(a)
    return new_list

# 2. 使用app.add_template_filter(函数名字, "模板名字")
app.add_template_filter(get_new_list,"my_filter1")

# 方式二:
# 直接定义视图函数使用@app.template_filter("模板名字")
@app.template_filter("my_filter2")
def get_new_list2(list):

    return [x + 1 for x in list]

@app.route('/')
def index():

    return render_template("file03.html",list=[x for x in range(0,10)])

if __name__ == "__main__":
    app.run(debug=True)