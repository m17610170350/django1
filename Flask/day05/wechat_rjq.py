#!/usr/bin/ python3
# -*-coding:utf-8-*-

from flask import Flask
import hashlib
import sys

from flask import request

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

TOKEN = "python25"


@app.route("/wechatrjq")
def wechat_rjq():
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")

    res_list = [timestamp, nonce, TOKEN]
    res_list.sort()

    res_str = "".join(res_list)

    res_sha1 = hashlib.sha1(res_str).hexdigest()

    if res_sha1 == signature:
        return echostr


if __name__ == '__main__':
    app.run(debug=True, port=8008)



