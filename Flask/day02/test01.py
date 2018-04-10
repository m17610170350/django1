#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
自定义转换器步骤:
1. 自定义类,继承自BaseConverter
2. 重写了__init__方法,重写父类方法super(类名,self).init(url_map)
3. 将规则赋值给子类

"""""

from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class MyConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(MyConverter, self).__init__(url_map)
        self.regex = regex


    # 一旦浏览器的参数符合指定规则的时候就会执行该方法, 在视图函数执行之前调用
    # 一般可以用来做一些处理,比如:转码等工作
    def to_python(self, value):
        return "to_python ++ %s"% value


app.url_map.converters["re"] = MyConverter
@app.route("/<re(r'\d+'):number>")
def index(number):

    return number

if __name__ == '__main__':
    app.run()