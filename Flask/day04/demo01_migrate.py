#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
在实际的开发中,往往都会有很多页面逻辑或者数据的增加,如果这个变化的过程,直接删除数据库在创建
就有可能造成数据的丢失,所以通过迁移可以很方便的记录每次变更的版本和数据
使用flask_migrate, flask_script
流程:
1. 创建数据库的管理对象Manager
2. 使用Migrate关联app和db
3. 给数据库的迁移添加一条命令, manager.add_command('db',MigrateCommand)

常见的操作命令:
1. 创建版本记录文件
python demo01migrate.py  db init

2. 创建迁移脚本,记录版本信息
python demo01migrate.py db migrate -m 'init db'

3. 跟新数据库
python demo01migrate.py db upgrade [version]

4. 降低数据库版本
python demo01migrate.py db  upgrade [version]

5. 查看当前的数据库的版本
python demo01migrate.py db current

6. 查看当前操作的数据库版本
python demo01migrate.py db  history
"""""

from flask import Flask

import sys

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

class DatabaseConfig:
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@localhost:3306/test03"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(DatabaseConfig)

db = SQLAlchemy(app)

# 创建app管理对象, 关联app
manager = Manager(app)
# 将app和db在此关联
Migrate(app, db)
# 给数据库的操作添加一条命令, 就是db
manager.add_command("db", MigrateCommand)



#创建模型类
class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(12))

@app.route("/")
def index():

    return "hello world"

if __name__ == '__main__':
    manager.run()










