# -*- coding: utf-8 -*-
# 配置文件
import redis


class Config(object):
    # mysql地址配置和消除警告
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zsj123456@localhost/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379

    # 配置SECREK_KEY
    '''
    随机盐值生成方式
    import os
    import base64
    base64.b64encode(os.urandom(32))
    '''
    SECRET_KEY = 'twgungBmRBakUm0WFrQf94YqkHbWcVCrKCq/r2OduNc='

    # 配置session存储到redis中
    PERMANENT_SESSION_LIFETIME = 60*60*24  # 单位是秒, 设置session过期的时间
    SESSION_TYPE = 'redis'  # 指定存储session的位置为redis
    SESSION_USE_SIGNER = True  # 对数据进行签名加密, 提高安全性
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 设置redis的ip和端口


# 上线模式
class ProductionConfig(Config):
    pass


# debug模式
class DevelopmentConfig(Config):
    DEBUG = True


# 测试模式
class TestingConfig(Config):
    TESTING = True

# 提供一个字典, 绑定关系
config_dict = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig,
    'testing': TestingConfig
}