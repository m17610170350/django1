#!/usr/bin/ python3
# -*-coding:utf-8-*-

from flask import Flask, session, make_response

import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
app.config["SECRET_KEY"] = "jifiahsijsaidhafhasjdoiasf"

@app.route("/set_session/<path:name>")
def set_session(name):
    # 设置session
    session["name"] = name

    return make_response("set_session")

@app.route("/get_session")
def get_session():
    name = session.get("name")
    return "get_session %s"%name

if __name__ == '__main__':
    app.run(debug=True)