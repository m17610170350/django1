# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf070862cc8e560162cd4fab5300be';

# 主帐号Token
accountToken = '12dc627d6efb439b9092685f8cb30103';

# 应用Id
appId = '8a216da862cc8f910162cd5303af00c9';

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com';

# 请求端口
serverPort = '8883';

# REST版本号
softVersion = '2013-12-26';


# 创建一个单利类
class CCP(object):
    # 重写__new__方法¨
    def __new__(cls, *args, **kwargs):
        # 判断cls是否有_instance属性, 如果没有,创建一个新的对象属性
        if not hasattr(cls, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # 初始化REST SDK
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
            return cls._instance

        return cls._instance

    # 发送短信方法
    def sendTemplateSMS(self, to, datas, tempId):

        result = self.rest.sendTemplateSMS(to, datas, tempId)

        # 如果返回的是0,则发送成功, 如果返回的是-1,则发送失败
        # print(result["statusCode"])
        if result["statusCode"] == "000000":

            return 0
        else:
            return -1

            # 发送模板短信
            # @param to 手机号码
            # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
            # @param $tempId 模板Id

            # def sendTemplateSMS(to,datas,tempId):
            #
            #
            #     #初始化REST SDK
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

            # sendTemplateSMS(手机号码,内容数据,模板Id)
