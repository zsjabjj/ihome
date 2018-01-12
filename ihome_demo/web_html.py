# -*- coding: utf-8 -*-
# 处理静态访问资源
from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

static_html = Blueprint('static_html', __name__)


# @static_html.route('/', methods=['GET', 'POST'])
# def index():
#     return current_app.send_static_file('html/index.html')

# 通过路由正则匹配
@static_html.route('/<re(r".*"):file_name>', methods=['GET', 'POST'])
def get_static_file(file_name):
    # print file_name + '1'
    if not file_name:
        file_name = 'index.html'
    # 如果文件名是'favicon.ico', 就直接返回
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name

    # 如果访问的页面, 紧跟着post/put/delete 都需要csrf_token.
    # 所以, 应该在访问任意网页时, 增加cookie
    # generate_csrf会检测当前session, 如果有, 则返回session中的. 如果没有, 则重新创建
    # Flask中从Session里的csrftoken取出来做对比
    csrf_token = generate_csrf()
    # print csrf_token + '2'
    response = make_response(current_app.send_static_file(file_name))
    response.set_cookie('csrf_token', csrf_token)
    # print file_name + '3'
    return response
