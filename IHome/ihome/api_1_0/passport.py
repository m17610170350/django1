#!/usr/bin/ python3
# -*-coding:utf-8-*-
import re
from flask import current_app
from flask import g
from flask import request, jsonify, json
from flask import session

from ihome import redis_store, db
from ihome.models import User
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from . import api


# 功能描述: 注册
# 请求路径: /api/v1.0/user
# 请求方式: POST
# 请求参数: 手机号, 短信验证码,密码
@api.route("/user", methods=["POST"])
def register_user():
    """
    1.获取参数
    2.校验参数
    3.根据手机号取出redis中的短信验证码
    4.判断短信验证码是否过期
    5.判断短信验证码是否正确
    6.创建user对象
    7.保存到数据库中
    8.可以记录用户登录状态(通过session)
    9.返回注册的结果给前端
    """""
    # 1.获取参数

    data_dict = request.json

    mobile = data_dict.get("mobile")
    phoneCode = data_dict.get("phoneCode")
    password = data_dict.get("password")

    # 2.校验参数

    if not all([mobile, phoneCode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"1[35678]\d{9}", mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号格式不正确")

    # 3.根据手机号取出redis中的短信验证码
    try:
        redis_sms_code = redis_store.get("sms_code:" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="短信验证码异常")

    # 4.判断短信验证码是否过期

    if not redis_sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码过期")

    # 5.判断短信验证码是否正确

    if redis_sms_code != phoneCode:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

    # 6.创建user对象

    user = User()
    user.name = mobile
    user.mobile = mobile
    # 加密密码
    # user.password_hash = user.password_jiami(password)
    user.password = password

    # 7.保存到数据库中
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="用户保存异常")

    # 8.可以记录用户登录状态(通过session)

    session["user_id"] = user.id
    session["user_name"] = user.name
    session["mobile"] = user.mobile

    # 9.返回注册的结果给前端

    return jsonify(errno=RET.OK, errmsg="注册成功")


#功能描述: 登录
#请求路径: /api/v1.0/session
#请求方式: POST
#请求参数: 用户名(手机号), 密码
@api.route("/session", methods=["POST"])
def login_user():
    """
    1.获取参数
    2.校验参数
    3.根据用户名取出用户对象
    4.判断用户对象是否存在
    5.判断密码是否正确
    6.记录用户的登录信息(使用session进行保存)
    7.返回登录信息给前端
    """
    # 1.获取参数
    data_dict = request.get_json()
    mobile = data_dict.get("mobile")
    password = data_dict.get("password")

    # 2.校验参数
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="账号密码不完整")

    try:
        number =  redis_store.get("login_user_error:"+mobile)
    except Exception as e:
        current_app.logger.error(e)
        number = 0

    try:
        number = int(number)
    except Exception as e:
        current_app.logger.error(e)
        number = 0

    if number >= 5:
        return jsonify(errno=RET.DATAERR,errmsg="十分钟之后再试")

    # 3.根据用户名取出用户对象
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="用户获取失败")


    # 4.判断用户对象是否存在
    if not user:
        return jsonify(errno=RET.DATAERR, errmsg="用户不存在")

    # 5.判断密码是否正确
    if not user.check_password(password):

        # 记录用户出错的次数 +1
        # incr 对存储在指定key的数值执行原子的加1操作。
        redis_store.incr("login_user_error" + mobile)
        # expire  设置key的过期时间，超过时间后，将会自动删除该key。
        redis_store.expire("login_user_error" + mobile, 10)

        return jsonify(errno=RET.DATAERR, errmsg="密码错误")

    # 6.记录用户的登录信息(使用session进行保存)
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["mobile"] = user.mobile

    # 7.返回登录信息给前端
    return jsonify(errno=RET.OK, errmsg="登录成功")

#功能描述: 显示首页的用户名
#请求路径: /api/v1.0/session
#请求方式: GET
#请求参数: 无
@api.route("/session")
@login_required
def get_user_name():
    # 1.获取到用户编号

    user_id = g.user_id

    # 2.到数据库中查询用户的对象信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")

    if not user:
        return jsonify(errno=RET.DATAERR, errmsg="该用户不存在")

    # 3.将用户对象内容,响应到前端页面中
    return jsonify(errno=RET.OK, errmsg="获取成功", data={"user_id":user_id, "name":user.name})


#功能描述: 登出登录
#请求路径: /api/v1.0/session
#请求方式: DELETE
#请求参数: 无
@api.route("/session", methods=["DELETE"])
def logout():
    # 1.删除session中的信息
    # 2.返回给前端页面
    session.clear()

    return jsonify(errno=RET.OK, errmsg="退出成功")