#!/usr/bin/ python3
# -*-coding:utf-8-*-
from functools import wraps

from flask import g
from flask import session, jsonify
from werkzeug.routing import BaseConverter

# 自定义转换器
from ihome.utils.response_code import RET


class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex


# 自定义登录装饰器
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):

        g.user_id = session.get("user_id")
        if g.user_id:
            return view_func(*args, **kwargs)
        else:
            return jsonify(errno=RET.USERERR, errmsg="用户尚未登录")
    return wrapper