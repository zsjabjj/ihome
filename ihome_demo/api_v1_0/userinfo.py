# -*- coding: utf-8 -*-
import logging

from flask import g, jsonify, request, session

from ihome_demo import db, constants
from ihome_demo.api_v1_0 import api
from ihome_demo.models import User
from ihome_demo.utils.common import login_required
from ihome_demo.utils.image_storage import storage
from ihome_demo.utils.response_code import RET

# 存储用户相关信息的接口

# 获取用户个人信息
# GET
# url: /api/v1_0/users
@api.route('/users', methods=['GET'])
@login_required
def get_user_info():
    user_id = g.user_id

    # 查询数据库 获取个人信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作, 用户不存在")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())

# 设置用户头像
# 使用七牛云对象存储
# POST
# url: /api/v1_0/users/avatar
@api.route('/users/avatar', methods=['POST'])
@login_required
def get_user_avatar():
    user_id = g.user_id
    # print user_id
    # 获取表单上传的头像图片
    avatar_file = request.files.get('avatar')

    # 校验参数
    if avatar_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg='未上传图像')

    # 上传七牛云, 获取二进制文件
    avatar_data = avatar_file.read()
    try:
        avatar_name = storage(avatar_data)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图像异常')

    # 保存图片路径到数据库
    try:
        # update: 查询之后拼接update, 可以直接进行更新操作
        # update中需要传入字典
        # 为了节省空间, 存数据库只存文件名. 域名可以自行拼接
        # user = User.query.get(user_id)
        # user.avatar_url = avatar_name
        # db.session.add(user)
        # 以上三步合并为如下一步, 使用update
        User.query.filter_by(id=user_id).update({'avatar_url':avatar_name})
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据库保存图像失败, 请重试')

    # 四. 返回数据
    # 返回给前端时, 需要拼接域名 , 返回一个完整的URL

    # 此时的文件名, 没有域名. 因此如果直接返回给客户端, 客户端无法直接加载
    # ozcxm6oo6.bkt.clouddn.com
    # 为了避免在数据库存储过多重复的域名前缀, 因此保存的时候, 不加域名. 返回给前端数据时, 我们拼接域名即可

    # 拼接完整的图像URL地址
    avatar_url = constants.QINIU_URL_DOMAIN + avatar_name

    # 返回的时候, 记得添加图像url信息
    # 如果还需要额外的返回数据, 可以再后方自行拼接数据, 一般会封装成一个字典返回额外数据
    return jsonify(errno=RET.OK, errmsg='保存图像成功', data={"avatar_url": avatar_url})

# 更改用户名
# PUT
# /api/v1_0/users/name
@api.route('/users/name', methods=['PUT'])
@login_required
def change_user_name():
    user_id = g.user_id
    # 获取用户想要设置的用户昵称
    req_dict = request.get_json()
    if not req_dict:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    name = req_dict.get('name')
    if name is None:
        return jsonify(errno=RET.PARAMERR, errmsg="名字不能为空")

    # 保存用户名到数据库
    try:
        User.query.filter_by(id=user_id).update({'name':name})
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="设置用户错误")

    # 修改session中的name字段
    session['user_name'] = name
    # print session.get('user_name')
    return jsonify(errno=RET.OK, errmsg="OK", data={"name": name})

# 设置实名认证
# POST
# URL: /api/v1_0/users/auth
@api.route('/users/auth', methods=['POST'])
@login_required
def set_user_auth():
    # 获取用户id
    user_id = g.user_id

    # 获取用户输入的实名认证信息
    req_dict = request.get_json()
    # print req_dict
    if req_dict is None:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 真实姓名real_name和身份证id_card
    real_name = req_dict.get('real_name')
    id_card = req_dict.get('id_card')
    # print real_name, id_card

    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # print 'haha'
    # 保存数据到数据库
    try:
        # update(real_name=real_name, id_card=id_card)
        # 报错:ERROR:root:update() got an unexpected keyword argument 'real_name'
        User.query.filter_by(id=user_id, real_name=None, id_card=None).update({'real_name':real_name, 'id_card':id_card})
        db.session.commit()
        # print 'heh'
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存用户实名信息失败")
    # print 'ok'
    return jsonify(errno=RET.OK, errmsg="OK")

# 获取实名认证的信息
# GET
# /api/v1_0/users/auth
@api.route('/users/auth', methods=['GET'])
@login_required
def get_user_auth():
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户实名信息失败")

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())


