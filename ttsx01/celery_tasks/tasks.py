from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired


app = Celery('celery_tasks.tasks', broker='redis://192.168.83.131:6379/4')

@app.task
def send_user_active(user):
    # 将账号信息进行加密
    serializer = Serializer(settings.SECRET_KEY, 60 * 60 * 2)
    value = serializer.dumps({'id': user.id})  # 返回bytes
    value = value.decode()  # 转成字符串，用于拼接地址

    # 向用户发送邮件
    msg = '<a href="http://127.0.0.1:8000/user/active/%s">点击激活</a>' % value
    send_mail('天天生鲜账户激活', '', settings.EMAIL_FROM, [user.uemail], html_message=msg)