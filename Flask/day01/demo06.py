#!/usr/bin/ python3
# -*-coding:utf-8-*-


"""
如果在通过浏览器访问视图函数的时候需要指定具体的参数个数类型,需要使用自定义转换器
自定义转换器的格式:
1. 自定类,继承BaseConverter
2. 重写__init__方法,接受三个参数
3. 重写父类方法
4. 将自定义的类,设置到app.url_map.converters["名字"]

"""""

from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)


# 自定义转换器
class MyConverterRegex(BaseConverter):
    # 自定义转化规则,需要将规则的url_map设置到父类
    def __init__(self, url_map, regex):
        super(MyConverterRegex, self).__init__(url_map)
        self.regex = regex

        # 将自定义的类,设置到app.url_map.converters["名字"]


app.url_map.converters["re"] = MyConverterRegex


# 使用自定义转换器匹配一个手机号
@app.route("/<re(r'1[35678]\d{9}'):mobile>")
def get_mobile(mobile):
    return "the mobile is %s" % mobile


# 使用自定义转换器匹配一个qq
@app.route("/qq/<re(r'[1-9]\d{4,9}'):qq>")
def get_qq(qq):
    return "the qq is %s" % qq


if __name__ == '__main__':
    app.run()
