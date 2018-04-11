#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
图书馆管理小项目:
展示:
作者名:
书名:
提交

----------------
作者A 删除
    书名1 删除
    书名2 删除

作者B 删除
    书名1 删除
    书名2 删除

流程:
1. 创建数据库,并设置数据库信息,模型编写
2. 表单创建,添加字段信息
3. 渲染到模板中

"""""

from flask import Flask,render_template
from flask import flash
from flask import redirect
from flask.ext.wtf import FlaskForm
from flask_sqlalchemy import  SQLAlchemy
from wtforms import StringField,SubmitField
from wtforms.validators import  DataRequired
import sys
reload(sys)
sys.setdefaultencoding("utf8")


app = Flask(__name__)

#配置数据库的信息
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:mysql@localhost:3306/test01"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] ="djkfkdfjd"

#创建管理对象
db = SQLAlchemy(app)

#编写模型类
# 作者 -> 书籍
class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    #关联属性
    books = db.relationship("Book",backref = "author", lazy="dynamic")

#书籍
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    #外键
    author_id = db.Column(db.Integer,db.ForeignKey(Author.id))

#创建添加数据表单
class AddBookForm(FlaskForm):
    author = StringField(label="作者", validators=[DataRequired()])
    book = StringField(label="书名", validators=[DataRequired()])
    submit = SubmitField(label="添加")


@app.route('/',methods=["GET","POST"])
def index():

    #1.创建表单
    bookForm = AddBookForm()


    #2.校验表单
    if bookForm.validate_on_submit():
        #2.1取出表单中的内容
        authorname = bookForm.author.data
        bookname = bookForm.book.data

        #2.2根据传入进来的作者名去数据中查看该作者是否存在
        author = Author.query.filter(Author.name == authorname).first()

        #判断作者是否存在
        if author:

            #2.3去数据库中查询书籍内容
            book = Book.query.filter(Book.name == bookname, Book.author_id == author.id).first()

            if book:
               flash("要添加的书籍已经存在")

            else:
                # 创建书籍对象,添加到数据库
                book = Book(name=bookname, author_id = author.id)
                db.session.add(book)
                db.session.commit()

        else: #作者不存在
            # 创建作者,添加
            author = Author(name=authorname)
            db.session.add(author)
            db.session.commit()

            # 创建书籍,添加
            book = Book(name = bookname, author_id = author.id)
            db.session.add(book)
            db.session.commit()

    #3.从数据库中查询作者信息
    authors = Author.query.all()

    return render_template("file_libaray.html",bookForm=bookForm,authors=authors)


@app.route('/delete_book/<int:id>')
def delete_book(id):
    #1.根据编号查询书籍
    book = Book.query.get(id)

    #2.删除
    db.session.delete(book)
    db.session.commit()

    #3.页面跳转
    return redirect("/")

@app.route('/delete_author/<int:id>')
def delete_author(id):

    #1.插叙作者
    author = Author.query.get(id)

    #2.删除作者对应的所有的书籍
    for book in author.books:
        db.session.delete(book)

    #3.删除作者
    db.session.delete(author)
    db.session.commit()

    #4.重定向到页面展示
    return redirect("/")



if __name__ == "__main__":

    #为了演示方便,先删除所有的数据
    db.drop_all()

    #创建所有的表
    db.create_all()

    #添加数据
    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老尹')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()

    app.run(debug=True)
