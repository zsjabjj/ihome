# -*- coding: utf-8 -*-
# from flask import Flask, request
#
# app = Flask(__name__)
#
# @app.route('/', methods=['GET', 'POST'])
# def hello_world():
#     a = request.get_json()
#
#     print type(a)
#     print a
#     return 'hello world!'
#
# if __name__ == '__main__':
#     app.run(debug=True)

from datetime import datetime
dt = datetime.now()
print   '时间：(%Y-%m-%d %H:%M:%S %f): ' , dt.strftime( '%Y-%m-%d %H:%M:%S %f' )
print   '时间：(%Y-%m-%d %H:%M:%S %p): ' , dt.strftime( '%y-%m-%d %I:%M:%S %p' )
print   '星期缩写%%a: %s '  % dt.strftime( '%a' )
print   '星期全拼%%A: %s '  % dt.strftime( '%A' )
print   '月份缩写%%b: %s '  % dt.strftime( '%b' )
print   '月份全批%%B: %s '  % dt.strftime( '%B' )
print   '日期时间%%c: %s '  % dt.strftime( '%c' )
print   '今天是这周的第%s天 '  % dt.strftime( '%w' )
print   '今天是今年的第%s天 '  % dt.strftime( '%j' )
print   '今周是今年的第%s周 '  % dt.strftime( '%U' )
print   '今天是当月的第%s天 '  % dt.strftime( '%d' )


'''
import os
import base64

from werkzeug.security import generate_password_hash, check_password_hash

from ihome_demo.models import User

a = base64.b64encode(os.urandom(32))
print a
b = generate_password_hash('123456')

print b
print check_password_hash(b, '123456')

user = User(name=12345678, mobile=12345678)
user.password = '123456'
print user.password
'''

# print user.password 执行后的结果
# Traceback (most recent call last):
#   File "E:/GitRepository/Flask/ihome/.test.py", line 18, in <module>
#     print user.password
#   File "E:\GitRepository\Flask\ihome\ihome_demo\models.py", line 39, in password
#     raise AttributeError('禁止访问用户密码')
# AttributeError: 禁止访问用户密码

# property装饰器的使用
# class Student(object):
#
#     @property
#     def score(self):
#         return self._score
#
#     @score.setter
#     def score(self, value):
#         if not isinstance(value, int):
#             raise ValueError('score must be an integer!')
#         if value < 0 or value > 100:
#             raise ValueError('score must between 0 ~ 100!')
#         self._score = value
#
# >>> s = Student()
# >>> s.score = 60 # OK，实际转化为s.set_score(60)
# >>> s.score # OK，实际转化为s.get_score()
# 60
# >>> s.score = 9999
# Traceback (most recent call last):
#   ...
# ValueError: score must between 0 ~ 100!