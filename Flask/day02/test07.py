#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
需求:
班主任,学习委员都向班长借钱, 但是班长没有钱,让找副班长,
但是副班长会根据不同的人借不同的钱数.
"""""

from flask import Flask
from flask import redirect
from flask import request
from flask import url_for

app = Flask(__name__)


@app.route("/banzhuren")
def ban_zhu_ren():
    return redirect(url_for("ban_zhang", id=233))


@app.route("/xuexiweiyuan")
def xue_xi_wei_yuan():
    return redirect(url_for("ban_zhang", id=333))


@app.route("/banzhang")
def ban_zhang():
    id = request.args.get("id")
    return redirect(url_for("fu_ban_zhang", id=id))


@app.route("/fubanzhang")
def fu_ban_zhang():
    id = request.args.get("id")
    if id == "233":
        return "ban_zhu_ren"
    elif id == "333":
        return "xue_xi_wei_yuan"


if __name__ == '__main__':
    app.run(debug=True)
