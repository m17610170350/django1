#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
宏(macro): 提前定义好了一段代码,在需要的时候执行和python中的函数类似
定义宏:
    {%macro 宏名(参数) %}

    {% endmacro %}

定义位置: 当前文件, 其他文件中

调用宏:
    当前文件: {{ 宏名(参数 )}}
    其他文件中:
        {% import '宏文件名 ' as 别名%}
        {{ 别名.宏名(参数) }}
"""""
from flask import Flask, render_template

import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

@app.route("/")
def index():

    return render_template("file_macro.html")

if __name__ == '__main__':
    app.run(debug=True)