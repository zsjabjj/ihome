# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-
import logging

from CCPRestSDK import REST
import ConfigParser

'''
ACCOUNT SID：8aaf07086077a6e60160b9a936b31a0e
AUTH TOKEN：557029db22e24f639659392b9f6ccddb
Rest URL(生产)：https://app.cloopen.com:8883
AppID(默认)：8aaf07086077a6e60160b9a937101a15
'''


# 主帐号
accountSid = '8aaf07086077a6e60160b9a936b31a0e'

# 主帐号Token
accountToken = '557029db22e24f639659392b9f6ccddb'

# 应用Id
appId = '8aaf07086077a6e60160b9a937101a15'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'

'''
1. to: 短信接收手机号码集合, 用英文逗号分开, 如'13810001000,13810011001', 最多一次发送200个。
2. datas：内容数据，需定义成列表方式，如模板中有两个参数，定义方式为array['验证码', '过期时间']。
3. temp_id: 模板Id, 如使用测试模板，模板id为"1"，如使用自己创建的模板，则使用自己创建的短信模板id即可。 
'''

# 使用单例, 实现运行过程中, 只进行一次鉴权
class CCP(object):
    def __new__(cls, *args, **kwargs):
        # 1. 判断是否有某个属性
        if not hasattr(cls, 'instance'):
            # 2. 调用父类方法, 创建一个对象
            cls.instance = super(CCP, cls).__new__(cls)
            # 初始化REST SDK, 鉴权操作
            cls.instance.rest = REST(serverIP, serverPort, softVersion)
            cls.instance.rest.setAccount(accountSid, accountToken)
            cls.instance.rest.setAppId(appId)
        return cls.instance

    def send_template_sms(self, to, datas, temp_id):
        # self: 这里的self就是cls.instance

        # 发送网络请求, 所以加try
        try:
            result = self.rest.sendTemplateSMS(to, datas, temp_id)
        except Exception as e:
            logging.error(e)
            raise e
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        # 主要的目的啊是从result获取statusCode的值. 如果是'000000'才是正确
        return result.get('statusCode')

                # sendTemplateSMS(手机号码,内容数据,模板Id)
if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms('18616784246', ['123456', '5'], 1)