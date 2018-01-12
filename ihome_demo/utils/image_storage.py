# -*- coding: utf-8 -*-

from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
from ihome_demo import constants

access_key = '8Eh8yqEXaDiItJYeZkpCHxtK7yF6VE-TlxBwosZM'
secret_key = 'k1mPJqG-Dhps9je4xeVCcx0n2sEk4EIp0SthjSgb'

# 我们使用此工具类的目的, 是调用存储图像方法后, 能够获得图像名-->给用户的用户头像路径赋值
def storage(file_data):
    """上传图片到七牛, file_data是文件的二进制数据"""
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'zsjihome'

    # 我们不需要这个Key. 七牛会自动生成
    # 上传到七牛后保存的文件名
    # key = 'my-python-logo.png';

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, constants.QINIU_UPLOAD_TOKEN_TIME)

    # 我们这个是通过form表单提交的, 不需要用到put_file方法
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, None, file_data)

    ret, info = put_data(token, None, file_data)

    print 'info: %s' % info
    print 'ret: %s' % ret

    if info.status_code == 200:
        # 表示上传成功， 返回文件名
        # 我们上传成功之后, 需要在别的页面显示图像, 因此需要返回图像名
        return ret.get("key")
    else:
        # 表示上传失败
        raise Exception("上传失败")
        # http://p24iqa82n.bkt.clouddn.com/FnTUusE1lgSJoCccE2PtYIt0f7i3


if __name__ == '__main__':
    # 打开图片数据
    # rb: 以二进制读
    with open("./girl2.jpg", "rb") as f:
        # 读取图片数据二进制数据
        file_data = f.read()
        # 上传图片书记到七牛云
        result = storage(file_data)
        # result 就存储的是图片名. 将来就可以再程序中调用显示
        print result

# info: exception:None, status_code:200, _ResponseInfo__response:<Response [200]>, text_body:{"hash":"FkKvjSTtbt3GyYksGsLnsFib5ruK","key":"FkKvjSTtbt3GyYksGsLnsFib5ruK"}, req_id:G3gAAH88EoNOOQcV, x_log:body:6;s.ph;s.put.tw:1;s.put.tr:9;s.put.tw:1;s.put.tr:14;s.ph;PFDS:16;PFDS:19;body;rs37_1.sel:34/not found;rs36_1.sel/not found;rdb.g/no such key;DBD/404;v4.get/Document not found;rs37_1.ins:18;rwro.ins:53;RS:54;rs.put:59;rs-upload.putFile:79;UP:98

# ret: {u'hash': u'FkKvjSTtbt3GyYksGsLnsFib5ruK', u'key': u'FkKvjSTtbt3GyYksGsLnsFib5ruK'}

# FkKvjSTtbt3GyYksGsLnsFib5ruK