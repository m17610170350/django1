#!/usr/bin/ python3
# -*-coding:utf-8-*-
from flask import current_app
from flask import g
from flask import request
from flask import session, jsonify

from ihome import constants
from ihome import db
from ihome.utils.image_storage import image_storage

from ihome.models import User
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from . import api


#功能描述: 展示个人信息
#请求路径: /api/v1.0/user
#请求方式: GET
#请求参数: 无
@api.route("/user")
@login_required
def get_user_info():
    # 1.获取到session中的手机号

    user_id = g.user_id

    if not user_id:
        return jsonify(errno=RET.DATAERR, errmsg="用户状态信息过期")

    # 2.根据手机号查询用户的个人信息
    try:
        user = User.query.filter(User.id == user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库失败")

    # 3.判断个人信息是否存在

    if not user:
        return jsonify(errno=RET.DATAERR, errmsg="该用户不存在")

    # 4.将个人信息转成字典格式



    #  5.将字典信息返回到前端页面展示
    return jsonify(errno=RET.OK, errmsg = "获取信息成功", data=user.user_to_dict())


#功能描述: 上传头像
#请求路径: /api/v1.0/user/avatar
#请求方式: POST
#请求参数: 头像
@api.route("/user/avatar", methods=["POST"])
@login_required
def image_upload():
    # 1.获取参数,头像, 用户编号

    user_id = g.user_id
    image_data = request.files.get("avatar").read()

    # 2.校验参数

    if not all([user_id, image_data]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 3.调用工具类上传头像

    try:
        image_name = image_storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="图片上传失败")

    # 4.通过用户编号获取到用户对象
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库存储异常")

    # 5.将图片名称更新到用户对象

    user.avatar_url = image_name

    # 6.提交用户对象到数据库中
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="图片保存失败")

    # 7.返回状态信息到前端页面

    avatar_url = constants.QINIU_DOMIN_PREFIX + user.avatar_url
    return jsonify(errno=RET.OK, errmsg="头像保存成功", data={"avatar_url":avatar_url})


#功能描述: 修改用户名
#请求路径: /api/v1.0/user/name
#请求方式: POST/PUT都可以
#请求参数: 无
@api.route("/user/name", methods=["PUT"])
@login_required
def set_user_name():
    # 1.获取用户编号,用户名

    user_id = g.user_id
    user_name = request.json.get("name")

    # 2.通过用户编号在数据库中查询用户对象
    try:
        user = User.query.filter(User.id == user_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据异常")


    # 3.判断用户是否存在

    if not user:
        return jsonify(errno=RET.DATAERR, errmsg="该用户不存在")

    # 4.将用户对象的信息用户名,进行更新

    user.name = user_name

    # 5.保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="更新数据有误")

    # 6.返回

    return jsonify(errno=RET.OK, errmsg="更改用户名成功")
