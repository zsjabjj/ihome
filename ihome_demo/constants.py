# -*- coding: utf-8 -*-

# 设置图片验证码在Redis中的过期时间, 三分钟后过期
IMAGE_CODE_REDIS_EXPIRE = 180

# 设置短信验证码在Redis中的过期时间, 三分钟后过期
SMS_CODE_REDIS_EXPIRE = 180

# 设置登录时输错信息, 达到上限后, 封锁ip的时间
LOGIN_ERROR_FORBID_TIME = 60 * 60 * 24

# 登录错误次数最大值
LOGIN_ERROR_MAX_NUM = 5

# 七牛云的访问域名
QINIU_URL_DOMAIN = "http://p24iqa82n.bkt.clouddn.com/"

# 上传七牛云token过期时间
QINIU_UPLOAD_TOKEN_TIME = 3600

# 城区信息的redis缓存时间， 单位：秒
AREA_INFO_REDIS_EXPIRES = 3600

# 首页展示最多的房屋数量
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的Redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页面每页的数量
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列表页面数据Redis缓存时间
HOUSE_LIST_PAGE_REDIS_EXPIRES = 3600

