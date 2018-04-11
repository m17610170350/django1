#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
falsk中本身没有提供数据库操作的功能,如果想要操作数据库,需要使用Flask_sqlalchemy扩展包

使用流程:
1. 导入模块
2. 配置数据链接信息
3. 自定模型类, 继承自db.Modle
4. 操作数据库

常见操作语句:
db.drop_all()   删除所有继承自db.Model类的表
db.create_all() 创建所有继承自db.Model类的表
db.session.add(obj) 添加单个对象
db.session.add_all([obj1,obj2....]) 添加多个对象
db.session.commit() 提交会话
db.session.rollback() 回滚


需求1: 如果知道用户对象的情况下,能不能够很方便的查询出,该用户关联的角色
     user.role

需求1: 如果知道角色对象的情况下,能不能够很方便的查询出,该角色关联的用户
     role.users

需要设置relationship关联方式

注意点:
1. 如果不设置模型类的__tablename__属性, 数据库中表的名字默认是模型类的小写
2. 如果是外键写在多方, 如果是relationship写在一方

"""""
# 1. 导入模块
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import not_, and_, or_
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
# 2. 配置数据链接信息
# 数据库链接
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:mysql@127.0.0.1:3306/test01"
# 设置true或者false都可以压制警告,如果设置为true会增加额外的开销
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 创建数据库管理对象,关联app应用程序
db = SQLAlchemy(app)


# 3. 自定模型类, 继承自db.Modle
class Role(db.Model):
    __tablename__ = "roles"
    # 设置id主键字段
    id = db.Column(db.Integer, primary_key=True)
    # 设置角色名属性,并且具有唯一性
    name = db.Column(db.String(64), unique=True)

    # 设置关联属性, 根据users可以直接获取所有关联的用户对象
    # 通过设置backref反向引用, 可以通过用户对象查询到扮演的角色
    # lazy如果设置成subquery,一旦获取到role角色的时候,马上就会把所有的用户都查询一遍
    # lazy如果设置成dynamic,只用用到users关联属性的时候才会去查询
    users = db.relationship("User", backref="roles", lazy="dynamic")

    # 为了输出对象的时候,方便看到对象的信息
    def __repr__(self):
        return "<Role:%s>" % self.name


class User(db.Model):
    __tablename__ = "users"
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    name = db.Column(db.String(64), unique=True)
    # 密码
    password = db.Column(db.String(128))
    # 邮箱
    email = db.Column(db.String(128))
    # 设置外检约束
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))

    # 为了输出对象的时候,方便看到对象的信息
    def __repr__(self):
        return "<Role:%s,%s,%s,%s>" % (self.name, self.password, self.email, self.role_id)


@app.route("/")
def index():

    return "index"


if __name__ == '__main__':
    # 为了演示方便, 先删除数据库中的表
    db.drop_all()

    # 创建所有继承自db.Model的模型类对应的表
    db.create_all()

    # 插入数据到数据中
    # 插入一条数据
    ro1 = Role(name="admin")
    db.session.add(ro1)
    db.session.commit()

    # 再次插入一条数据
    ro2 = Role(name='user')
    db.session.add(ro2)
    db.session.commit()

    # 一次插入多条数据
    us1 = User(name='wang', email='wang@163.com', password='123456', role_id=ro1.id)
    us2 = User(name='zhang', email='zhang@189.com', password='201512', role_id=ro2.id)
    us3 = User(name='chen', email='chen@126.com', password='987654', role_id=ro2.id)
    us4 = User(name='zhou', email='zhou@163.com', password='456789', role_id=ro1.id)
    us5 = User(name='tang', email='tang@itheima.com', password='158104', role_id=ro2.id)
    us6 = User(name='wu', email='wu@gmail.com', password='5623514', role_id=ro2.id)
    us7 = User(name='qian', email='qian@gmail.com', password='1543567', role_id=ro1.id)
    us8 = User(name='liu', email='liu@itheima.com', password='867322', role_id=ro1.id)
    us9 = User(name='li', email='li@163.com', password='4526342', role_id=ro2.id)
    us10 = User(name='sun', email='sun@163.com', password='235523', role_id=ro2.id)
    db.session.add_all([us1, us2, us3, us4, us5, us6, us7, us8, us9, us10])
    db.session.commit()

    app.run(debug=True)
