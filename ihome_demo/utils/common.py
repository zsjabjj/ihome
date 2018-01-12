# -*- coding: utf-8 -*-
# 正则转换器
from functools import wraps

from flask import session, g, jsonify
from werkzeug.routing import BaseConverter
from ihome_demo.utils.response_code import RET


# 自定义正则转换器
class RegexConverter(BaseConverter):
    # 重新init方法, 增加参数
    # regex: 就是在使用时, 传入的正则表达式
    def __init__(self, url_map, regex):
        # 调用父类方法
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex

# 自定义检测用户是否登录的装饰器
# 去session中获取数据 id
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # 获取已登录用户的id保存到g变量中, 以便之后使用
        user_id = session.get('user_id')
        if user_id is not None:
            # 表示用户已经登录
            # 使用g对象保存user_id，在视图函数中可以直接使用
            # 比如后面设置头像的时候, 仍然需要获取session的数据.
            # 为了避免多次访问redis服务器. 可以使用g变量
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            # 用户未登录
            resp = {
                "errno": RET.SESSIONERR,
                "errmsg": "用户未登录"
            }
            return jsonify(resp)
    return wrapper

