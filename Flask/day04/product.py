#!/usr/bin/ python3
# -*-coding:utf-8-*-
from flask import Blueprint

#创建蓝图对象, 参数1: 表示蓝图的名字, 参数2, 表示当前模块的蓝图
product = Blueprint("product",__name__)

#使用蓝图对象装饰视图函数
@product.route("/get_product_info")
def get_product_info():
    return "get_product_info"