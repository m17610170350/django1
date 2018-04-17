# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8aaf070862cc8e560162cd4fab5300be';

# ���ʺ�Token
accountToken = '12dc627d6efb439b9092685f8cb30103';

# Ӧ��Id
appId = '8a216da862cc8f910162cd5303af00c9';

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com';

# ����˿�
serverPort = '8883';

# REST�汾��
softVersion = '2013-12-26';


# ����һ��������
class CCP(object):
    # ��д__new__������
    def __new__(cls, *args, **kwargs):
        # �ж�cls�Ƿ���_instance����, ���û��,����һ���µĶ�������
        if not hasattr(cls, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # ��ʼ��REST SDK
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
            return cls._instance

        return cls._instance

    # ���Ͷ��ŷ���
    def sendTemplateSMS(self, to, datas, tempId):

        result = self.rest.sendTemplateSMS(to, datas, tempId)

        # ������ص���0,���ͳɹ�, ������ص���-1,����ʧ��
        # print(result["statusCode"])
        if result["statusCode"] == "000000":

            return 0
        else:
            return -1

            # ����ģ�����
            # @param to �ֻ�����
            # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
            # @param $tempId ģ��Id

            # def sendTemplateSMS(to,datas,tempId):
            #
            #
            #     #��ʼ��REST SDK
            #     rest = REST(serverIP,serverPort,softVersion)
            #     rest.setAccount(accountSid,accountToken)
            #     rest.setAppId(appId)
            #
            #     result = rest.sendTemplateSMS(to,datas,tempId)
            #     for k,v in result.iteritems():
            #
            #         if k=='templateSMS' :
            #                 for k,s in v.iteritems():
            #                     print '%s:%s' % (k, s)
            #         else:
            #             print '%s:%s' % (k, v)
            #

            # sendTemplateSMS(�ֻ�����,��������,ģ��Id)
