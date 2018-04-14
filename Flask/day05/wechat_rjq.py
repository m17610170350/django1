#!/usr/bin/ python3
# -*-coding:utf-8-*-

from flask import Flask
from flask import request
import hashlib
import sys


reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

token = "python25"


@app.route("/wechat8008")
def wechat_rjq():
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")
    # 1）将token、timestamp、nonce三个参数进行字典序排序
    params = [token,timestamp,nonce]
    params.sort()

    # 2）将三个参数字符串拼接成一个字符串进行sha1加密
    params_str = "".join(params)
    signature2 = hashlib.sha1(params_str).hexdigest()

    # 3）开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if signature == signature2:
        return echostr
    else:
        ""

if __name__ == '__main__':
    app.run(debug=True, port=8008)
