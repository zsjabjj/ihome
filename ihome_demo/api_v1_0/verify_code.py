# -*- coding: utf-8 -*-
import logging
import random

from flask import jsonify, make_response, request
from ihome_demo import redis_store, constants
from ihome_demo.api_v1_0 import api
from ihome_demo.libs.cloudsdk.sms import CCP
from ihome_demo.models import User
from ihome_demo.utils.captcha.captcha import captcha
from ihome_demo.utils.response_code import RET

'''
开发流程:
产品经理设计好了原型图, 给了需求
一. 先后台再前端
1. 自行开发接口(定义路由, 实现视图函数)
2. 测试接口(postman/浏览器/单元测试)
3. 编写API文档
4. 让前端根据文档进行开发

二. 前后端一起开发
1. 前后端一起交流, 定义出简易API文档, 及符合此文档的JSON数据.
2. 前后端分别开发
3. 后端先测试, 然后让前端测试
4. 完善API文档
'''


# 专门处理验证码

# 图片验证码, URL设计风格符合RESTful风格
# url: 127.0.0.1:5000/api/v1_0/image_codes/<image_code_id>

# 参数: image_code_id

# 返回: image图像

# 格式: JSON

@api.route('/image_codes/<image_code_id>')
def get_img_code(image_code_id):
    # print '1'
    # 1. 获取参数, 参数通过网址中获取
    # 客户端生成UUID
    # 2. 对参数做完整性校验
    # 如果能进入此路由, 说明一定是传递了参数, 所以不就省去了判断是否为空的判断
    # 3. 处理业务逻辑
    # 3.1 生成验证码
    # 图片名name  验证码内容text  验证码图片(图片二进制文件)image_data
    name, text, image_data = captcha.generate_captcha()
    # print name
    # 3.2 保存到Redis中
    # 保存到数据库的时候, 有可能会出现异常保存不成功, 所以需要try
    try:
        # key--->'image_code_' + image_code_id
        # setex--->set + expire
        # setex中需要传三个参数
        # 第一个参数: key
        # 第二个参数: 过期时间(单位是秒)
        # 第三个参数: value(验证码内容)
        redis_store.setex('image_code_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRE, text)
    except Exception as e:
        logging.error(e)
        # 返回错误信息
        return jsonify({
            'errno': RET.DBERR,
            'errmsg': '数据库发生异常, 请重试'
        })
    # 4. 处理返回值 contet-type : text/html --> image/jpg
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    print response
    return response

# 获取短信验证码
# URL 127.0.0.1:5000/api/v1_0/sms_codes/17612345678?image_code=1234&image_code_id=1234156

# 手机号: mobile
# 图片验证码:image_code
# UUID:image_code_id

# GET
@api.route('/sms_codes/<re(r"1[3456789][0-9]{9}"):mobile>')
def get_sms_code(mobile):
    # 获取参数
    # 普通参数获取
    image_code = request.args.get('image_code')
    image_code_id = request.args.get('image_code_id')

    # 校验参数
    if not all([image_code, image_code_id]):
        return jsonify({
            'errno': RET.PARAMERR,
            'errmsg': '参数不完整, 请重新填写'
        })

    # 逻辑处理
    # 和Redis数据对比
    # 获取Redis数据, 判断是否为空
    try:
        real_image_code = redis_store.get('image_code_%s' % image_code_id)
    except Exception as e:
        logging.error(e)
        return jsonify({
            'errno': RET.DBERR,
            'errmsg': '数据库查询异常'
        })

    if real_image_code is None:
        return jsonify({
            'errno': RET.NODATA,
            'errmsg': '验证码已失效或已删除'
        })

    # 无论图片验证码正确与否, 只能使用一次, 就需要删除
    try:
        redis_store.delete('image_code_%s' % image_code_id)
    except Exception as e:
        logging.error(e)

    # 和用户传入的图片验证码数据对比, 注意: 大小写, 这里统一转换成小写
    if image_code.lower() != real_image_code.lower():
        return jsonify({
            'errno': RET.DATAERR,
            'errmsg': '验证码输入有误'
        })

    # 判断用户是否注册过, 判断是否为空
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
    else:
        if user is not None:
            return jsonify({
                'errno': RET.DATAEXIST,
                'errmsg': '此号码已被注册'
            })

    # 发送短信验证码
    # 自行生成验证码, 06d: 要求6位数, 不足以0补齐
    sms_code = '%06d' % random.randint(0, 999999)

    # 保存到Redis数据库中
    try:
        redis_store.setex('sms_code_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRE, sms_code)
    except Exception as e:
        logging.error(e)
        return jsonify({
            'errno': RET.DBERR,
            'errmsg': '访问数据库发生异常'
        })

    # 调用云通讯接口, 发送验证码
    ccp = CCP()
    try:
        status_code = ccp.send_template_sms(mobile, [sms_code, str(constants.SMS_CODE_REDIS_EXPIRE / 60)], 1)
    except Exception as e:
        logging.error(e)
        return jsonify({
            'errno': RET.THIRDERR,
            'errmsg': '发送短信验证码失败'
        })

    # 返回数据
    if status_code == '000000':
        return jsonify({
            'errno': RET.OK,
            'errmsg': '发送短信验证码成功'
        })
    else:
        return jsonify({
            'errno': RET.THIRDERR,
            'errmsg': '发送短信验证码失败'
        })
