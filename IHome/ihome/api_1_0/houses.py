#!/usr/bin/ python3
# -*-coding:utf-8-*-
import datetime
from flask import current_app, jsonify
from flask import g
from flask import json
from flask import request

from ihome import constants
from ihome import redis_store, db
from ihome.utils.commons import login_required
from ihome.utils.image_storage import image_storage
from ihome.utils.response_code import RET

from ihome.api_1_0 import api
from ihome.models import Area, House, Facility, HouseImage, Order

# 功能:获取城区信息
"""
#功能描述：　获取城区信息
#请求路径：　/api/v1.0/areas
#请求方式: GET
#请求参数: 无"""


@api.route("/areas")
def get_area():
    # 先到redis中查询是否有城区信息
    areas = redis_store.get("areas")

    if areas:
        area_dict = json.loads(areas)
        return jsonify(errno=RET.OK, errmsg="获取城区信息成功", data=area_dict)

    # 1.查询数据库的城区信息
    try:
        area_list = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

    if not area_list:
        return jsonify(errno=RET.DATAERR, errmsg="查询不到城区信息")

    # 2.将城区信息转成字典列表

    area_dict = []
    for area in area_list:
        area_dict.append(area.to_dict())

    # 将城区信息存储在redis缓存中
    try:
        redis_store.set("areas", json.dumps(area_dict))
    except Exception as e:
        current_app.logger.error(e)

    # 3.响应给前端页面

    return jsonify(errno=RET.OK, errmsg="查询成功", data=area_dict)


# 发布房屋的基本信息
# 功能描述: 发布房屋的基本信息
# 请求路径: /api/v1.0/houses
# 请求方式: POST
# 请求参数: 价格,标题...等等
@api.route("/houses", methods=["POST"])
@login_required
def send_house_info():
    # 1.获取用户编号

    user_id = g.user_id

    # 2.获取房屋的基本信息, 设施信息
    data_dict = request.json
    title = data_dict.get("title")
    price = data_dict.get("price")
    area_id = data_dict.get("area_id")
    address = data_dict.get("address")
    room_count = data_dict.get("room_count")
    acreage = data_dict.get("acreage")
    unit = data_dict.get("unit")
    beds = data_dict.get("beds")
    deposit = data_dict.get("deposit")
    min_days = data_dict.get("min_days")
    max_days = data_dict.get("max_days")
    facilities = data_dict.get("facility")

    # 3.校验参数

    if not all([title, price, area_id, address, room_count, acreage, unit, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 4.房屋价格, 押金的整数处理
    # 由于在使用支付宝支付的时候,最小单位是分, 所以保存在数据库中的价格,单位是分
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数格式不正确")

    # 5.创建房屋对象

    house = House()

    # 6.将房屋的基本信息设置到房屋对象中

    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    # 7.通过设施信息,取出设置列表,设置到房屋对象中

    facilities = Facility.query.filter(Facility.id.in_(facilities)).all()
    house.facilities = facilities

    # 8.设置房屋的主人

    house.user_id = user_id

    # 9.更新内容数据库

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存数据库失败")

    # 10.返回,携带房屋编号

    return jsonify(errno=RET.OK, errmsg="基本信息保存成功", data={"house_id": house.id})


# 功能描述: 发布房屋图片
# 请求路径: /api/v1.0/houses/<int:house_id>/images
# 请求方式: POST
# 请求参数: 房屋图片
@api.route("/houses/<int:house_id>/images", methods=["POST"])
@login_required
def send_house_image(house_id):
    # 1.获取house_id
    # 2.获取到图片
    image_data = request.files.get("house_image").read()

    # 3.根据房屋编号获取到房屋对象
    try:
        house = House.query.filter(House.id == house_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询房屋失败")

    if not house:
        return jsonify(errno=RET.DATAERR, errmsg="该房屋不存在")

    # 4.上传图片到七牛云
    try:
        image_url = image_storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="七牛云上传失败")

    # 5.设置房屋的默认图像图像
    if not house.index_image_url:
        house.index_image_url = image_url

    # 6.创建房屋图片对象
    house_image = HouseImage()

    # 7.设置图片对象的房屋编号
    house_image.house_id = house_id
    house_image.url = image_url

    # 8.更新数据库
    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存房屋图片失败")

    # 9.返回,携带图片的url
    house_image_url = constants.QINIU_DOMIN_PREFIX + image_url
    return jsonify(errno=RET.OK, errmsg="上传图片信息成功", data={"url": house_image_url})


# 功能描述: 获取热门房源
# 请求路径: /api/v1.0/houses/index
# 请求方式: GET
# 请求参数: 无
@api.route("/houses/index")
def get_houses_index():
    # 1.查询数据库,排名前5的所有房子
    try:
        houses = House.query.order_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

    # 2.将对象列表转成字典列表

    house_list = []
    if houses:
        for house in houses:
            house_list.append(house.to_basic_dict())

    # 3.响应给前端, 带上字典列表
    return jsonify(errno=RET.OK, errmsg="获取成功", data=house_list)


# 功能描述:搜索房源
# 请求路径：/api.v1.0/houses
# 请求方式：GET
# 请求参数：区域编号，开始时间，结束时间，排序关键字，分页
@api.route("/houses")
def search_house():
    # 1.获取参数

    # current_app.logger.debug(request.args)
    aid = request.args.get("aid")

    # booking(订单量), price-inc(低到高), price-des(高到低), new:安装房子的创建时间
    sk = request.args.get("sk")
    p = request.args.get("p", 1)
    sd = request.args.get("sd", "")
    ed = request.args.get("ed", "")

    # 参数校验
    try:
        p = int(p)

        # 将时间字符串转成日期对象
        start_date = None
        end_date = None

        if sd:
            # 将时间字符串,按照指定的格式转成日期对象
            start_date = datetime.datetime.strptime(sd, "%Y-%m-%d")

        if ed:
            end_date = datetime.datetime.strptime(ed, "%Y-%m-%d")

        if start_date and end_date:
            assert start_date <= end_date, Exception("开始时间不能大于结束")

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数格式异常")

    #查询redis,看是否有缓存数据
    try:
        redis_key = "search_%s_%s_%s_%s" % (aid, sk, sd, ed)
        resp = redis_store.hget(redis_key, p)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询缓存失败")

    # 如果查到数据.直接进行返回
    if resp:
        return jsonify(errno=RET.OK, errmsg="从缓存中获取成功", data=eval(resp))

    # 2.查询房源
    try:
        house_query = House.query
        # 2.1判断区域编号
        if aid:
            house_query = house_query.filter(House.area_id == aid)

        # 增加时间条件,选出冲突订单
        conflict_orders = []
        if start_date and end_date:
            conflict_orders = Order.query.filter(start_date < Order.end_date, end_date > Order.begin_date)
        elif start_date:
            conflict_orders = Order.query.filter(start_date < Order.end_date)
        elif end_date:
            conflict_orders = Order.query.filter(end_date > Order.begin_date)

        # 2.1.3通过冲突的订单找出冲突的房子编号, 然后添加到查询条件中
        if conflict_orders:
            conflict_house_id = [order.house_id for order in conflict_orders]
            house_query = house_query.filter(House.id.notin_(conflict_house_id))

        # 2.2判断排序的方式
        if sk == "booking":
            house_query = house_query.order_by(House.order_count.desc())

        elif sk == "price-inc":
            house_query = house_query.order_by(House.price.asc())

        elif sk == "price-des":
            house_query = house_query.order_by(House.price.desc())

        else:
            house_query = house_query.order_by(House.create_time.desc())

        # 3.增加分页方式
        paginate = house_query.paginate(page=p, per_page=constants.HOUSE_LIST_PAGE_CAPACITY)
        # 获取当前页面房屋数量
        houses = paginate.items
        # 获取总页数
        total_page = paginate.pages

        # 执行查询
        # houses = house_query.all()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

    # 3.将房子对象列表 转换成字典列表

    house_list = []
    if houses:
        for house in houses:
            house_list.append(house.to_basic_dict())

    resp = {"houses": house_list, "total_page": total_page}

    # 通过redis缓存房屋数据
    try:
        pipeline = redis_store.pipeline()  # 获取管道对象, 用来做事物操作
        # 开始事务
        pipeline.multi()
        redis_key = "search%s_%s_%s_%s" % (aid, sk, sd, ed)

        # 存储数据, 并设置有效期
        redis_store.hset(redis_key, p, resp)
        redis_store.expire(redis_key, constants.HOUSE_LIST_REDIS_EXPIRES)

        # 提交事务
        pipeline.execute()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据缓存异常")

    # 4.响应，携带房源信息
    return jsonify(errno=RET.OK, errmsg="获取房屋成功", data=resp)
