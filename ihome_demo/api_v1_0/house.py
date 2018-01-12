# -*- coding: utf-8 -*-

import logging

from datetime import datetime
from flask import json, jsonify, request, g, session

from ihome_demo import redis_store, constants, db
from ihome_demo.api_v1_0 import api
from ihome_demo.models import Area, House, Facility, HouseImage, User, Order
from ihome_demo.utils.common import login_required
from ihome_demo.utils.image_storage import storage
from ihome_demo.utils.response_code import RET




# 城区信息查询
# GET
# /api/v1_0/areas
@api.route('/areas', methods=['GET'])
def get_area_info():
    """
    1. 访问redis获取缓存
    2. 没有缓存, 查询MySQL
    3. 需要对数据转JSON
    4. 保存redis中
    5. 如果有缓存, 返回缓存数据
    6. 返回给浏览器
    """
    try:
        areas_json = redis_store.get('area_info')
    except Exception as e:
        logging.error(e)
        # 这里不需要返回错误信息, 因为没有会直接查询数据库
        # 为了避免异常的事情发生, 如果执行失败, 就把数据设置为None
        areas_json = None

    # 没有缓存, 查询数据库
    if areas_json is None:
        # 查询数据库中城区信息
        areas_list = Area.query.all()
        # print areas_list
        # 想给前端传递数据格式为
        # "data": {"areas":[{"aid": 1,"aname": "东城区"},{"aid": 2,"aname": "西城区"}]}
        areas_dict = {"areas":[area.to_dict() for area in areas_list]}
        # print areas_dict

        # json dict--->json str
        areas_json = json.dumps(areas_dict)
        # print areas_json
        # 将数据保存到数据库Redis中
        try:
            redis_store.setex('area_info', constants.AREA_INFO_REDIS_EXPIRES, areas_json)
        except Exception as e:
            logging.error(e)
            # 这里只是对数据进行Redis缓存, 如果没有数据, 就会去mysql数据库中读取数据

    # 返回数据

    # return '{"errno":RET.OK, "errmsg": "查询城区信息成功", "data": %s}' % areas_json
    # RET.OK 直接使用返回不了数据
    # return jsonify({"errno":RET.OK, "errmsg": "查询城区信息成功", "data": areas_json})
    # 前面已经将区域数据转为JSON了. 这里不需要再次调用jsonify来返回, 直接返回字典格式的信息即可

    return '{"errno": %s, "errmsg": "查询城区信息成功", "data": %s}' % (RET.OK, areas_json)


# 发布新房源
# 保存房屋信息
# POST
# URL: /api/v1_0/houses/info
@api.route('/houses/info', methods=['POST'])
@login_required
def save_house_info():
    """保存房屋的基本信息
    前端发送过来的json数据
    {
        "title":"",
        "price":"",
        "area_id":"1",
        "address":"",
        "room_count":"",
        "acreage":"",
        "unit":"",
        "capacity":"",
        "beds":"",
        "deposit":"",
        "min_days":"",
        "max_days":"",
        "facility":["7","8"]
    }
    """

    # 获取参数
    house_dict = request.get_json()
    if house_dict is None:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    title = house_dict.get("title")  # 房屋名称标题
    price = house_dict.get("price")  # 房屋单价
    area_id = house_dict.get("area_id")  # 房屋所属城区的编号
    address = house_dict.get("address")  # 房屋地址
    room_count = house_dict.get("room_count")  # 房屋包含的房间数目
    acreage = house_dict.get("acreage")  # 房屋面积
    unit = house_dict.get("unit")  # 房屋布局（几室几厅)
    capacity = house_dict.get("capacity")  # 房屋容纳人数
    beds = house_dict.get("beds")  # 房屋卧床数目
    deposit = house_dict.get("deposit")  # 押金
    min_days = house_dict.get("min_days")  # 最小入住天数
    max_days = house_dict.get("max_days")  # 最大入住天数
    # 基础设施后续进行处理

    # 参数校验
    if not all([title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断单价和押金格式是否正确, 有可能从前端传递过来的不是数字, 例如:123.--
    # 前端传送过来的金额参数是以元为单位，浮点数，数据库中保存的是以分为单位，整数
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="单价和押金输入有误")

    # 保存房屋信息
    # 创建房屋对象
    user_id = g.user_id
    house = House(
        user_id=user_id,
        area_id=area_id,
        title=title,
        price=price,
        address=address,
        room_count=room_count,
        acreage=acreage,
        unit=unit,
        capacity=capacity,
        beds=beds,
        deposit=deposit,
        min_days=min_days,
        max_days=max_days
    )

    # 处理房屋的设施信息, 获取房屋设施信息
    # 如果有就保存到house对象中, 如果没有就直接返回
    facility_id_list = house_dict.get('facility')

    # 再去查询数据库中是否存在, 避免前端传递错误数据, 相当于参数校验
    if facility_id_list:
        try:
            facility_list = Facility.query.filter(Facility.id.in_(facility_id_list)).all()
        except Exception as e:
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库查询异常')
        # 查询到数据后, 将数据添加到house中
        if facility_list:
            house.facilities = facility_list

    # 保存数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据库添加异常')

    # 返回数据
    # 这里需要返回房屋id信息, 因为发布成功后, 会进入发布房屋图片的界面
    # 设置图片, 必须知道房屋的id才行
    return jsonify(errno=RET.OK, errmsg='新房源信息添加成功', data={'house_id':house.id})


# 添加房源图片
# POST
# URL: /api/v1_0/houses/<int:house_id>/images
@api.route('/houses/<int:house_id>/images', methods=['POST'])
@login_required
def save_house_image(house_id):
    """保存房屋的图片"""
    # 获取参数 房屋的图片、房屋编号
    # house_id = request.form.get("house_id")
    image_file = request.files.get("house_image")

    # 校验参数
    if not all([house_id, image_file]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 1. 判断房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库异常')

    if house is None:
        return jsonify(errno=RET.NODATA, errmsg='房屋不存在')

    # 2. 上传房屋图片到七牛中
    image_data = image_file.read()
    try:
        image_name = storage(image_data)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图片失败')

    # 3. 保存图片信息到数据库中
    house_image = HouseImage(house_id=house_id, url=image_name)
    db.session.add(house_image)

    # 4. 处理房屋基本信息中的主图片
    if not house.index_image_url:
        house.index_image_url = image_name
        db.session.add(house)

    # 5. 统一提交数据
    try:
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='提交数据异常')

    # 返回数据
    image_url = constants.QINIU_URL_DOMAIN + image_name
    return jsonify(errno=RET.OK, errmsg='上传图片成功', data={'image_url':image_url})


# 显示我的房源中的信息
# GET
# url: /api/v1_0/users/houses
@api.route('/users/houses', methods=['GET'])
@login_required
def get_user_houses():
    # 获取user_id
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
        houses = user.houses
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取数据失败")

    houses_list = list()
    if houses:
        for house in houses:
            houses_list.append(house.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg="OK", data={"houses": houses_list})


# 房屋详情页面
# GET
# /api/v1_0/houses/<int:house_id>
@api.route('/houses/<int:house_id>', methods=['GET'])
def get_house_detail(house_id):
    """获取房屋详情"""
    # 前端在房屋详情页面展示时，如果浏览页面的用户不是该房屋的房东，则展示预定按钮，否则不展示，
    # 所以需要后端返回登录用户的user_id
    # 尝试获取用户登录的信息，若登录，则返回给前端登录用户的user_id，否则返回user_id=-1
    user_id = session.get("user_id", "-1")

    # 校验参数
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数缺失")

    # 先从redis缓存中获取信息
    try:
        ret = redis_store.get("house_info_%s" % house_id)
    except Exception as e:
        logging.error(e)
        ret = None
    if ret:
        logging.info("hit house info redis")
        return '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, ret), 200, {"Content-Type": "application/json"}

    # 查询数据库
    try:
        house = House.query.get(house_id)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

    # 将房屋对象数据转换为字典
    try:
        house_dict = house.to_full_dict()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="数据出错")

    # 存入到redis中
    json_house = json.dumps(house_dict)
    try:
        redis_store.setex("house_info_%s" % house_id, constants.HOUSE_DETAIL_REDIS_EXPIRE_SECOND, json_house)
    except Exception as e:
        logging.error(e)

    resp = '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, json_house)
    return resp


# 首页轮播图片
# GET
# /api/v1_0/houses/index
@api.route('/houses/index', methods=['GET'])
def get_house_index():
    '''获取主页幻灯片展示的房屋基本信息'''
    # 从缓存中尝试获取数据
    try:
        ret = redis_store.get('home_page_data')
    except Exception as e:
        logging.error(e)
        ret = None
    if ret:
        logging.info('hit house info redis')
        return '{"errno":0, "errmsg":"OK", "data":%s}' % ret

    # 缓存中没有数据, 查询数据库, 将热门的5条数据展示出来
    try:
        # 查询数据库, 返回房屋订单数据最多的5条数据
        houses = House.query.order_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    if houses is None:
        return jsonify(errno=RET.NODATA, errmsg='查询无数据')

    # 以'data':{'data1':[{}, {}, {}...]}数据格式传递数据给前端
    houses_list = list()
    for house in houses:
        # 如果房屋未设置主图片, 则跳过
        if not house.index_image_url:
            continue
        houses_list.append(house.to_basic_dict())
    # 将数据转换为json, 并保存到Redis
    json_houses = json.dumps(houses_list)
    # print '-'*30
    # print json_houses
    # print '-'*30
    # print type(json_houses)

    try:
        redis_store.setex('home_page_data', constants.HOME_PAGE_DATA_REDIS_EXPIRES, json_houses)
    except Exception as e:
        logging.error(e)

    return '{"errno":0, "errmsg":"OK", "data":%s}' % json_houses


# 房屋数据搜索
# GET
# URL: /api/v1_0/houses?sd=xxxx-xx-xx&ed=xxxx-xx-xx&aid=xx&sk=new&p=1
# sd==startDate, ed==endDate, aid==areaId, sk==sortKey, p==next_page
@api.route("/houses", methods=["GET"])
def get_house_list():
    """获取房屋列表信息"""
    # 一. 获取参数
    # 注意: 参数可以不传, 不传就把参数设为空值或者默认值
    # 获取起始时间
    start_date_str = request.args.get('sd', '')
    # 获取结束时间
    end_date_str = request.args.get('ed', '')
    # 获取排序关键字
    sort_key = request.args.get('sk', 'new')
    # 获取城区信息
    area_id = request.args.get('aid', '')
    # 获取页数
    page = request.args.get('p', 1)

    # 二. 校验参数
    # 2.1判断日期
    # 需要确保能够转换成日期类, 且开始时间不能大于结束时间
    try:
        # 需要确保能够转换成日期类
        start_date = None
        # print start_date_str --> 2018-01-11
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            # print start_date --> 2018-01-11 00:00:00

        end_date = None
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        if start_date and end_date:
            # 开发期间, 可以通过增加断言来帮助调错
            assert start_date <= end_date
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')


    # 2.2判断页数
    # 需要确保页数能够转为int类型
    try:
        page = int(page)
    except Exception as e:
        page = 1

    # 三. 业务逻辑处理

    # 3.1 先从redis缓存中获取数据
    # 如果获取了数据, 可以直接返回, 不需要执行下面逻辑
    redis_key = 'houses_%s_%s_%s_%s' % (start_date_str, end_date_str, area_id, sort_key)
    try:
        # 保存数据时, 在Redis中使用的是hash, 取的时候用hget
        resp_json = redis_store.hget(redis_key, page)
    except Exception as e:
        logging.error(e)
        resp_json = None
    if resp_json:
        # 有缓存就直接返回
        return resp_json

    # 3.2 定义查询数据的参数空列表
    # 为了方便设置过滤条件, 先定义空列表, 然后逐步判断添加进来
    # House.query.filter_by([这中间拼接筛选条件]).all()
    filter_params = list()

    # 3.3 处理区域信息
    if area_id:
        # 数据库框架内部重写了==的__eq__函数
        # House.area_id == area_id 结果是SQL对象
        filter_params.append(House.area_id==area_id)

    # 3.4 处理时间, 获取不冲突的房屋信息
    # 需要根据传入的时间参数不同, 获取冲突的房屋, 再从房屋中获取对应的房屋ID
    try:
        conflict_orders_li = list()
        if start_date and end_date:
            # 从订单表中查询冲突的订单, 进而获取冲突的房屋id
            # 查询结束时间大于订单开始时间, 查询开始时间小于订单结束时间,
            # 在查询时, 被预定的就不能被查询出来, 这就是冲突房屋
            conflict_orders_li = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= start_date).all()
        elif start_date:
            conflict_orders_li = Order.query.filter(Order.end_date >= start_date).all()
        elif end_date:
            conflict_orders_li = Order.query.filter(Order.begin_date <= end_date).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')

    if conflict_orders_li:
        # 提取出冲突房屋的id
        conflict_house_id_li = [order.house_id for order in conflict_orders_li]
        # 添加条件, 查询不冲突房屋
        filter_params.append(House.id.notin_(conflict_house_id_li))

    # 定义查询语句, 将filter_params传入
    # House.query.filter_by(*filter_params).order_by()

    # 3.5 排序
    # 不同的排序, 过滤条件不同
    # sort_key = 'booking' --> 入住最多
    # sort_key = 'price-inc' --> 价格低 -> 高
    # sort_key = 'price-des' --> 价格高 -> 低
    # new 默认 -> 最新发布的

    if sort_key == 'booking':
        # 如果没有跟上all(), first(), paginate()
        # 以下代码只是过滤条件
        house_query = House.query.filter(*filter_params).order_by(House.order_count.desc())
    elif sort_key == 'price-inc':
        house_query = House.query.filter(*filter_params).order_by(House.price.asc())
    elif sort_key == 'price-des':
        house_query = House.query.filter(*filter_params).order_by(House.price.desc())
    else:
        house_query = House.query.filter(*filter_params).order_by(House.create_time.desc())

    # 3.6 分页  sqlalchemy的分页
    # 在之前房屋的过滤条件后面, 使用paginate设置分页
    # paginate三个参数: 当前要查询的页码, 每页数量, 是否要返回错误信息
    try:
        house_page = house_query.paginate(page, constants.HOUSE_LIST_PAGE_CAPACITY, False)
        # print house_page --> <flask_sqlalchemy.Pagination object at 0x0000000005527278>
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')

    # 获取总页数
    total_page = house_page.pages
    # 获取当前页数
    # house_page.page

    # 获取分页的数据, 需要调用items
    house_li = house_page.items
    # print house_li  ---> [<ihome_demo.models.House object at 0x0000000005530EF0>, <ihome_demo.models.House object at 0x0000000005530F98>]

    # 3.7 将数据转为JSON
    # 定义一个空列表, 遍历拼接转换后的模型数据
    houses = list()
    for house in house_li:
        houses.append(house.to_basic_dict())

    resp = dict(errno=RET.OK, errmsg='查询成功', data={'houses':houses, 'total_page':total_page, 'current_page':page})
    resp_json = json.dumps(resp)

    # 3.8 将结果缓存到redis中
    # 用redis的哈希类型保存分页数据, 并使用事务提交保存
    # 传入的页码超过了最大页数 6>5
    if page <= total_page:
        redis_key = 'houses_%s_%s_%s_%s' % (start_date_str, end_date_str, area_id, sort_key)

        try:
            # 这里使用事务提交, 两个操作必须同时执行才行
            # 如果使用事务提交, 失败了, 就会自动回滚
            pipeline = redis_store.pipeline()

            # 开启事务
            pipeline.multi()
            # 保存数据
            pipeline.hset(redis_key, page, resp_json)
            # 设置缓存过期时间
            pipeline.expire(redis_key, constants.HOUSE_LIST_PAGE_REDIS_EXPIRES)
            # 执行事务
            pipeline.execute()
        except Exception as e:
            logging.error(e)

    # 四. 数据返回
    return resp_json
