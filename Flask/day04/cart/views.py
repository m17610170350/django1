#coding:utf8

#从当前文件中找cart模块,如果没有找__init__文件
from . import cart
from flask import render_template

#2.使用蓝图装饰视图函数
@cart.route('/get_cart_info')
def get_cart_info():
    return "cart_info"


#3.设置渲染汽车信息
@cart.route('/show_cart')
def show_cart():

    return render_template("file02cart.html")
