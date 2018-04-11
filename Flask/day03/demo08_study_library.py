#!/usr/bin/ python3
# -*-coding:utf-8-*-

from flask import Flask, render_template
from flask.ext.wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy

import sys

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
# 1. 创建数据库,并设置数据库信息,模型编写
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:mysql@127.0.0.1:3306/test02"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "laizhongshishishabi"


# 创建管理对象
db = SQLAlchemy(app)

#编写模型类
# 作者 -> 书籍
class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    # 关联属性
    books = db.relationship("Book", backref = "author", lazy = "dynamic")


# 书籍
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # 外键
    author_id = db.Column(db.ForeignKey(Author.id))


# 创建添加数据的表单
class AddBookForm(FlaskForm):
    author = StringField(label="作者", validators=[DataRequired()])
    book = StringField(label="书名", validators=[DataRequired()])
    submit = SubmitField(label="添加")



@app.route("/", methods=["GET", "POST"])
def index():
    #1.创建表单
    bookForm = AddBookForm()


    # 校验表单
    if bookForm.validate_on_submit():
        # 取出表单中的数据
        authorname = bookForm.author.data
        bookname = bookForm.book.data

        # 根据表单中传进来的作者名去数据库中查看该作者是否存在
        author = Author.query.filter(Author.name == authorname).first()

        # 判断作者是否存在
        if author:

            # 去数据库中查看该书籍的信息
            book = Book.query.filter(Book.name == bookname, Book.author_id == author.id).first()
            



    authors = Author.query.all()
    return render_template("file_study_libaray.html", bookForm = bookForm, authors=authors)

if __name__ == '__main__':

    #为了演示方便,先删除所有的数据
    db.drop_all()

    #创建所有的表
    db.create_all()

    #添加数据
    # 生成数据
    au1 = Author(name='何老')
    au2 = Author(name='张老')
    au3 = Author(name='老赖')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='赖总回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让赖总变得更骚', author_id=au2.id)
    bk4 = Book(name='赖总征服了美丽少男', author_id=au3.id)
    bk5 = Book(name='赖总回忆是怎样征服了美丽少男',author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()

    app.run(debug=True)