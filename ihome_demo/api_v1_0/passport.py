# -*- coding: utf-8 -*-
import logging
import re

from flask import request, jsonify, session
from ihome_demo import redis_store, db, constants
from ihome_demo.api_v1_0 import api
from ihome_demo.models import User
from ihome_demo.utils.common import login_required
from ihome_demo.utils.response_code import RET


# POST
# URL: /api/v1_0/users/
# 按照RESTful设计风格, 在路由设置时, 需要根据操作的资源来去路由名, 此处是对用户信息进行操作, 故选择users来做路由
# 手机号   mobile
# 短信验证码 sms_code
# 密码    password
# 数据    json



# 注册
@api.route('/users', methods=['POST'])
def register():
    # 1, 获取数据 post请求, json数据
    # 前端给的是json字符串, 后端通过get_json获取后, 结果为字典, 在get_json方法中已经做了loads处理
    # 也可以使用request.data获取, 不过取到的是json字符串, 需要使用loads转换为字典, 方便取值
    request_dict = request.get_json()
    # print request_dict
    mobile = request_dict.get('mobile')
    sms_code = request_dict.get('sms_code')
    password = request_dict.get('password')
    # print mobile, sms_code, password
    # 2, 校验数据
    # 完整性
    if not all([mobile, sms_code, password]):
        return jsonify({'errno': RET.PARAMERR, 'errmsg': '信息不能有空'})

    # 手机号正则
    if not re.match(r'1[3456789]\d{9}', mobile):
        return jsonify({'errno': RET.PARAMERR, 'errmsg': '手机号码输入不全'})

    # 3, 业务逻辑处理
    # try:从redis中获取短信验证码
    try:
        real_sms_code = redis_store.get('sms_code_%s' % mobile)
    except Exception as e:
        logging.error(e)
        return jsonify({'errno': RET.DBERR, 'errmsg': '数据库查询出错'})

    # 判断验证码是否过期
    if real_sms_code is None:
        return jsonify({'errno': RET.NODATA, 'errmsg': '验证码已过期'})

    # 判断用户是否输入了正确的验证码
    if sms_code != real_sms_code:
        return jsonify({'errno': RET.DATAERR, 'errmsg': '验证码输入有误'})

    # try:删除短信验证码(如果验证出错重新发送的话, 浪费资源, 浪费用户时间) 跟之前的发送短信验证码3,4步是相反的
    try:
        redis_store.delete('sms_code_%s' % mobile)
    except Exception as e:
        logging.error(e)

    # 把数据保存到数据库(如果重复注册, 会导致失败)
    # 创建用户, 保存数据
    user = User(name=mobile, mobile=mobile)

    # 密码的处理, 应该交给模型类去处理, 在models中设置了密码加密
    user.password = password

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify({'errno': RET.DBERR, 'errmsg': '保存数据出错'})

    # 保存将来需要用到的session数据, 达到状态保持
    # db.session: 处理数据库的
    # Session (大写的, flask_session的) 将session数据从以前默认的cookie, 存放到redis中
    # session: flask自带的session, 这个才是用来设置数据的
    # 如果在前端设置注册成功后跳转到首页, 此处就需要进行状态保持
    # 如果在前端设置注册成功后跳转到登录页面, 此处就可以省略状态保持, 可以到登录页面的路由去处理
    # 此处就跳转到登录页
    # session['user_id'] = user.id
    # session['mobile'] = mobile
    # session['user_name'] = mobile

    # 4, 返回值, 注册成功返回的页面, 交由前端处理

    return jsonify({'errno': RET.OK, 'errmsg': '注册成功'})


# 登录
# POST
# URL: /api/v1_0/sessions
# 按照RESTful设计风格, 在路由设置时, 需要根据操作的资源来去路由名, 此处是对用户信息进行操作, 故选择users来做路由
# 手机号   mobile
# 密码    password
# 数据    json


@api.route('/sessions', methods=['POST'])
def login():
    # 1, 获取数据
    request_dict = request.get_json()
    mobile = request_dict.get('mobile')
    password = request_dict.get('password')

    # 2, 校验数据
    if not all([mobile, password]):
        return jsonify({'errno': RET.PARAMERR, 'errmsg': '信息不能有空'})

    # 手机号正则
    if not re.match(r'1[3456789]\d{9}', mobile):
        return jsonify({'errno': RET.PARAMERR, 'errmsg': '手机号码输入不全'})

    # 3, 逻辑处理
    '''
    1. 登录需要判断和记录错误次数, 登录错误次数过多, 在redis中记录该手机号或者IP
    如果超过了最大次数, 就直返返回, 不需要执行登录逻辑

    2. 判断用户名(查询数据库)和密码(验证密码)是否正确, 设置错误次数INCR key, 同时设置有效期

    3. 登录成功, 删除redis的错误数据

    4. 设置session
    '''
    # 3.1
    user_ip = request.remote_addr  # 获取用户访问时的ip地址
    print user_ip
    try:
        # 获取用户输入错误次数, 获得的access_count结果类型为字符串
        access_count = redis_store.get('access_count_%s' % user_ip)
    except Exception as e:
        logging.error(e)
        return jsonify({'errno': RET.DBERR, 'errmsg': '访问数据库出错'})

    # 获取到了数据, and 次数没有超过最大值. 假设最大次数为5
    if access_count is not None and int(access_count) >= constants.LOGIN_ERROR_MAX_NUM:
        return jsonify({'errno': RET.REQERR, 'errmsg': '登录次数已达上限, 24小时后重试'})

    # 3.2
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
        return jsonify({'errno': RET.DBERR, 'errmsg': '访问数据库出错'})
    # user不存在 or 密码检查没通过  --> 用户名或密码错误
    if user is None or not user.check_password(password):
        try:
            # incr 执行一次, 增加一, 数据为str类型
            redis_store.incr('access_count_%s' % user_ip)
            # 设置错误5次输入后, 封锁ip的时间, 例如登录次数已达上限, 24小时后重试
            redis_store.expire('access_count_%s' % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            logging.error(e)
            return jsonify({'errno': RET.DBERR, 'errmsg': '添加登录错误次数和过期时间出错'})
        return jsonify({'errno': RET.LOGINERR, 'errmsg': '用户名或密码错误, 你还有%s次登录机会' % str(5-int(access_count))})

    # 3.3
    try:
        redis_store.delete('access_count_%s' % user_ip)
    except Exception as e:
        logging.error(e)

    # 3.4
    session['user_id'] = user.id
    session['mobile'] = mobile
    session['user_name'] = user.name

    # 4, 返回数据
    return jsonify({'errno': RET.OK, 'errmsg': '登录成功'})

# 检查登录状态
# GET
# URL: /api/v1_0/sessions

@api.route('/sessions', methods=['GET'])
def check_login():
    # 从session中获取用户名
    name = session.get('user_name')
    print name
    # # 判断用户名是否存在
    # if name is None:
    #     return jsonify({'errno': RET.SESSIONERR, 'errmsg':'用户未登录'})
    # else:
    #     return jsonify({'errno': RET.OK, 'errmsg':'用户已登录', 'data':{'name':name}})
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")

# 登出
# DELETE
# URL: /api/v1_0/sessions
# 登出前需要先判断是否是登录状态
# 需要自定义一个判断是否为登录的装饰器
# 登出就是清除掉用户的session
@api.route('/sessions', methods=['DELETE'])
@login_required
def logout():
    # 清除数据前, 需要将csrf_token保留
    # location.href = '/login.html'   location.href 只是页面内跳转, 网页不会刷新. 如果不刷新, 无法设置csrf_token.
    csrf_token = session.get('csrf_token')
    print csrf_token
    session.clear()
    session['csrf_token'] = csrf_token
    return jsonify(errno=RET.OK, errmsg='OK')