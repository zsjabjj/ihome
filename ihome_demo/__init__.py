# -*- coding: utf-8 -*-
# 创建APP用的
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_dict, Config

from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from ihome_demo.utils.common import RegexConverter

# 将参数延后传入的技巧
# 问题抛出: 有些对象, 外界需要应用. 但是这个对象又必须在app创建之后
# 解决方案: 可以先创建该对象, 在app创建之后, 再设置app


db = SQLAlchemy()

csrf = CSRFProtect()

redis_store = None

# 项目日志
'''
日志的级别
ERROR: 错误级别
WARN: 警告级别
INFO: 信息界别
DEBUG: 调试级别

平时开发, 可以使用debug和info替代print, 来查看对象的值
上线时, 不需要删除这个日志, 只需要更改日志的级别为error/warn
'''
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器, 指明日志保存的路径, 每个日志文件的最大大小, 保存的日志文件个数上限
file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名  行数       日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象(flask app使用的) 添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 提供一个函数来创建app, 同时提供参数, 让外界传入
def create_app(config_name):

    # 管理app的创建
    app = Flask(__name__)

    # 导入配置参数
    app.config.from_object(config_dict[config_name])

    # 创建数据库
    db.init_app(app)

    global redis_store
    # redis, 最优方式是将参数写到配置文件
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

    # 给app的路由转换器字典增加我们自定义的转换器
    app.url_map.converters['re'] = RegexConverter

    # csrf保护
    # 用postman测试时, 需要暂时关闭csrf保护
    # 不然会报错: The CSRF token is missing
    csrf.init_app(app)

    # Session
    # 创建能够将默认存放在cookie的sesion数据, 转移到redis的对象
    # http://pythonhosted.org/Flask-Session/
    Session(app)

    # 注册蓝图
    # 为了解决循环导入的问题, 需要将蓝图的导入延后导入.
    # url_prefix访问地址前添加的前缀
    from ihome_demo.api_v1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1_0')

    from ihome_demo import web_html
    app.register_blueprint(web_html.static_html)


    return app, db
