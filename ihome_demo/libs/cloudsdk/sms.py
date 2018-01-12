# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-
import logging

from CCPRestSDK import REST
import ConfigParser

'''
ACCOUNT SID��8aaf07086077a6e60160b9a936b31a0e
AUTH TOKEN��557029db22e24f639659392b9f6ccddb
Rest URL(����)��https://app.cloopen.com:8883
AppID(Ĭ��)��8aaf07086077a6e60160b9a937101a15
'''


# ���ʺ�
accountSid = '8aaf07086077a6e60160b9a936b31a0e'

# ���ʺ�Token
accountToken = '557029db22e24f639659392b9f6ccddb'

# Ӧ��Id
appId = '8aaf07086077a6e60160b9a937101a15'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'

'''
1. to: ���Ž����ֻ����뼯��, ��Ӣ�Ķ��ŷֿ�, ��'13810001000,13810011001', ���һ�η���200����
2. datas���������ݣ��趨����б�ʽ����ģ�������������������巽ʽΪarray['��֤��', '����ʱ��']��
3. temp_id: ģ��Id, ��ʹ�ò���ģ�壬ģ��idΪ"1"����ʹ���Լ�������ģ�壬��ʹ���Լ������Ķ���ģ��id���ɡ� 
'''

# ʹ�õ���, ʵ�����й�����, ֻ����һ�μ�Ȩ
class CCP(object):
    def __new__(cls, *args, **kwargs):
        # 1. �ж��Ƿ���ĳ������
        if not hasattr(cls, 'instance'):
            # 2. ���ø��෽��, ����һ������
            cls.instance = super(CCP, cls).__new__(cls)
            # ��ʼ��REST SDK, ��Ȩ����
            cls.instance.rest = REST(serverIP, serverPort, softVersion)
            cls.instance.rest.setAccount(accountSid, accountToken)
            cls.instance.rest.setAppId(appId)
        return cls.instance

    def send_template_sms(self, to, datas, temp_id):
        # self: �����self����cls.instance

        # ������������, ���Լ�try
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
        # ��Ҫ��Ŀ�İ��Ǵ�result��ȡstatusCode��ֵ. �����'000000'������ȷ
        return result.get('statusCode')

                # sendTemplateSMS(�ֻ�����,��������,ģ��Id)
if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms('18616784246', ['123456', '5'], 1)