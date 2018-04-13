#!/usr/bin/ python3
# -*-coding:utf-8-*-


import unittest

from flask import json

from demo07_login import app

class LoginTest(unittest.TestCase):

    #每次测试之前都会走该方法
    #在该方法中可以做一些初始化的操作,比如: 数据库的链接,测试模式的开启
    def setUp(self):
        self.client = app.test_client()
        #开启调试模式, 如果不开启测试模式只会报测试案例的错误, 如果开启了会报错相应错误信息提示
        app.testing = True


    def test_username_password_empry(self):
        #1.获取测试客户端
        # client = app.test_client()

        #2.发送请求,传递参数
        resp =  self.client.post("/login",data={"username":"","password":"dfjkdjfkdf"})

        #3.将响应response对象解析字典数据
        resp_josn = resp.data
        resp_dict = json.loads(resp_josn)

        #4.断言, 是否包含errcode字段
        self.assertIn("errcode",resp_dict,"must have errcode")

        #5.取出errcode
        errcode = resp_dict.get("errcode")

        #6.断言, errcode必须是-2
        self.assertEqual(errcode,-2,"errcode must be -2, current is %d"%errcode)


    def test_username_password_iscorrect(self):
        # 1.获取测试客户端
        # client = app.test_client()

        # 2.发送请求,传递参数
        resp = self.client.post("/login", data={"username": "admin", "password": "123"})

        # 3.将响应response对象解析字典数据
        resp_josn = resp.data
        resp_dict = json.loads(resp_josn)

        # 4.断言, 是否包含errcode字段
        self.assertIn("errcode", resp_dict, "must have errcode")

        # 5.取出errcode
        errcode = resp_dict.get("errcode")

        # 6.断言, errcode必须是0
        self.assertEqual(errcode, 0, "errcode must be 0, current is %d" % errcode)

