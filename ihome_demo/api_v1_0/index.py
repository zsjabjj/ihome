# -*- coding: utf-8 -*-
import logging

from . import api
# 在此处导入models, 解决:No changes in schema detected.问题
# 因为创建好models后, 在不使用的情况下, 没有模块知道它的存在
from ihome_demo import models


# 定义路由
@api.route('/', methods=['GET', 'POST'])
def index():
    # 打印日志
    logging.debug('debug')
    logging.info('info')
    logging.warn('warn')
    logging.error('error')
    return 'index'
