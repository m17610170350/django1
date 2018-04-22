#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
第一步:
1.数据库配置,数据库迁移等
2.配置redis
3.配置session
4.csrf保护机制
5.日志信息等

第二步:
项目分层

第三步:
视图函数,业务逻辑编写

设置模板文件:
file --settings-->edit_keymap -->live template -->flask -->点击添加

注意点:
1. csrf机制会对POST,PUT,DELETE,PATCH进行保护
2. flask_session用来指定session的存储位置
"""""
from flask.ext.migrate import MigrateCommand, Migrate
from flask_script import Manager
from ihome import create_app, db


# 创建 app，并传入配置模式：development / production
app = create_app("development")
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    # print app.url_map
    manager.run()
