#!/usr/bin/ python3
# -*-coding:utf-8-*-
# 生成图片验证码, 短信验证码


# 功能描述: 获取图片验证码
# 请求路径: /api/v1.0/image_code
# 请求方式:GET
# 请求参数: 图片验证码编号
import random
import re

from flask import current_app, jsonify
from flask import json
from flask import make_response
from flask import request
from ihome.utils.captcha.captcha import captcha

from ihome import constants
from ihome import redis_store
from ihome.utils.response_code import RET
from ihome.utils.sms import CCP
from . import api


@api.route("/image_code")
def get_image_code():
    """
    1.获取到请求的参数
    2.生成图片验证码
    3.保存图片验证码到redis中
    4.返回响应信息
    """
    # 1.获取到请求的参数
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")

    # 2.生成图片验证码
    name, text, imageData = captcha.generate_captcha()

    # 3.保存图片验证码到redis中
    # redis_store.set(key, value, 过期时间)
    try:
        redis_store.delete("image_code" + pre_id)
        redis_store.set("image_code" + cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据操作异常")

    response = make_response(imageData)
    response.headers["Content-Type"] = "image/jpg"
    return imageData


# 功能描述: 发送短信验证码
# 请求路径: /api/v1.0/sms_code
# 请求发送: POST
# 请求参数:手机号,图片验证码A, 图片验证码编号

@api.route("/sms_code",methods=["POST"])
def get_sms_code():
    """
    1.获取请求的参数
    2.判断参数是否为空
    3.判断手机号的格式是否正确
    4.根据图片验证码编号取出redis中的图片验证码B
    5.判断验证码A,B是否相等
    6.创建要发送的短信验证码
    6.调用方法发送短信
    7.将短信验证码存储到redis中
    8.返回获取状态给前端页面
    :return:
    """
    # 1.获取请求的参数
    json_data =  request.data
    dict_data = json.loads(json_data)

    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.get("image_code_id")

    # 2.判断参数是否为空
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    # 3.判断手机号的格式是否正确
    if not re.match(r"1[35678]\d{9}",mobile):
        return jsonify(errno=RET.DATAERR,errmsg="手机号格式错误")

    # 4.根据图片验证码编号取出redis中的图片验证码B
    try:
        redis_image_code = redis_store.get("image_code"+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据操作异常")

    if not redis_image_code:
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码过期")

    #删除redis中的图片验证码,不然用户重复填同一个来验证
    try:
        redis_store.delete("image_code:"+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码操作异常")

    # 5.判断验证码A,B是否相等
    if image_code != redis_image_code:
        return jsonify(errno=RET.DATAERR,errmsg="图片验证错误")

    # 6.创建要发送的短信验证码
    sms_code = "%06d"%random.randint(0,999999)

    # 7.调用方法发送短信
    try:
        ccp = CCP()
        result = ccp.sendTemplateSMS(mobile,[sms_code,5],1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg="短信发送失败")

    #判断是否有发送成功
    if result == -1:
        return jsonify(errno=RET.DATAERR,errmsg="短信发送失败")

    # 8.将短信验证码存储到redis中
    try:
        redis_store.set("sms_code:"+mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="短信验证码存储异常")

    # 9.返回获取状态给前端页面
    return jsonify(errno=RET.OK,errmsg="发送成功")

