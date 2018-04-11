#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
传统表单: 是由一堆的html标签组成的,维护起来特别繁琐, 比如需要给标签添加过滤,验证过程复杂

flask中提供了关于表单操作的扩展包: flask_wtforms 通过扩展表单可以很方便的对标签的验证,过滤进行操作
好处:
    1. 验证表单标签方便
    2. 加入csrf机制的验证

操作流程:
1. 导入模块
2. 创建自定义类,继承FlaskForm
3. 编写字段信息,填写校验函数
4. 创建表单对象,渲染到模板中

注意点:
1. 表单的验证机制需要设置csrf_token
2. csrf_token依赖了SECRET_KEY,需要设置
3. csrf验证机制会对以下请求方式产生校验: PSOT,DELETE,PUT,DSIPATCH校验
4. 获取数据方式: 表单对象.字段名.data获取数据

"""""
from flask import Flask, render_template, request, url_for

import sys

from flask.ext.wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
app.config["SECRET_KEY"] = "woainiqingaidezuguo"

@app.route("/index", methods=["POST", "GET"])
def index():

    #1.获取表单提交过来的参数
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("password2")

    # 2. 参数验证
    if request.method == "POST":
        if not all([username, password, password2]):
            return "内容不完整"

        # 3. 判断密码是否一致
        if password == password2:
            # 假设注册成功了
            return "注册成功"
        else:
            riderict = url_for("index")
            return "密码不正确,点击<a href="+ riderict +">返回</a>注册页面"

    return render_template("file_normal_form.html")


#自定一个类,继承自FlaskForm
class RegisterForm(FlaskForm):
    username = StringField(label="用户名", validators=[DataRequired()],render_kw={"placeholder":"请输入用户名"})
    password = PasswordField(label="密码",validators=[DataRequired()])
    password2 = PasswordField(label="确认密码",validators=[DataRequired(),EqualTo("password","error")])
    submit = SubmitField(label="提交")


@app.route("/index2", methods=["POST", "GET"])
def index2():

    # 1. 创建表单
    registerform = RegisterForm()

    # 2. 校验
    if registerform.validate_on_submit():
        # 原生获取内容方式:
        # username = request.form.get("username")
        # password = request.form.get("password")
        # password2 = request.form.get("password2")

        #wtform表单提供的获取字段方式
        username = registerform.username.data
        password = registerform.password.data
        password2 = registerform.password2.data

        print username, password, password2
        return "注册成功"
    return render_template("file_normal_form.html", registerform=registerform)


if __name__ == '__main__':
    app.run(debug=True)






