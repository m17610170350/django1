#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
在服务器向客户端返回数据的时候如何指定一个json格式的数据,有两种方式:
1.将字典转换成json对象返回
    dict = {
        "name":"zhangsan",
        "age":13
    }
    resp = jsonify(dict)
    return resp

2. 直接使用参数的形式,传递到jsonify(key=value,key1=value1)中
    resp = jsonify(key=value,key1=value1)
    return resp

查看5000端口是否被占用:
lsof -i:5000

如果有运行占用的端口kill即可

"""""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def get_json():
    # 1.将字典转换成json对象返回
    # dict = {
    #     "name": "zhangsan",
    #     "age": 13
    # }
    # resp = jsonify(dict)
    # return resp

    # 2. 直接使用参数的形式，传递到jsonify（key=value， key=value）
    resp = jsonify(name="lisi", moeny=999, sex='girl')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
