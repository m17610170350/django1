#!/usr/bin/ python3
# -*-coding:utf-8-*-
from flask import Blueprint

#1. 创建蓝图对象
#2. 如果指定了templates和根路径中的templates是同名的文件夹, 那么同名文件访问的时候默认就是根路径的
#  如果模块中的文件名和根路径中的文件名一样,默认访问的是根路径的资源
cart = Blueprint("cart", __name__,
                 template_folder="cartxxx",
                 static_folder="static",
                 static_url_path="/static",
                 # url_prefix="/cart" #指定该蓝图的访问前缀
                 )

from . import views
