#!/usr/bin/ python3
# -*-coding:utf-8-*-

"""
如果想要使用邮件发送,需要使用到扩展flask_mail, 里面提供了两个类,Mail,Message
发送流程:
0. 配置邮件发送配置信息
1. 创建邮件发送客户端对象
2. 创建消息体,设置内容
3. 调用send方法发送邮件
"""""
from threading import Thread

from flask import Flask
from flask_mail import Mail, Message
import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

# 配置邮件：服务器／端口／安全套接字层／邮箱名／授权码
app.config['MAIL_SERVER'] = "smtp.163.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "m17610170350@163.com"
app.config['MAIL_PASSWORD'] = "qian7426"
app.config["MAIL_DEFAULT_SENDER"] = "m17610170350@163.com"

#创建邮箱客户端
mail = Mail(app)

# 使用异步线程发送
def send_mail_async(app, message):
    with app.app_context():  # 开启上下文环境
        import time
        time.sleep(10)
        mail.send(message)


@app.route("/send_mail")
def send_mail():

    message = Message()
    message.subject = "赖总好帅哦" # 邮件的主题
    message.recipients = ["m17610170350@163.com"]
    message.body = "Trending in film, music and books this week"

    # mail.send(message)

    thread = Thread(target=send_mail_async, args=(app, message))
    thread.start()

    return "发送成功233"

if __name__ == '__main__':
    app.run(debug=True)