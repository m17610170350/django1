from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import UserInfo
import re
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from django.core.mail import send_mail


# Create your views here.
def register(request):
    """返回注册页面"""
    return render(request, 'register.html')


class RegisterView(View):
    """类视图：处理注册"""

    def get(self, request):
        """处理GET请求，返回注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        uname = request.POST.get('user_name')
        upwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        uemail = request.POST.get('email')
        uallow = request.POST.get('allow')

        # print(uname, upwd, cpwd, uemail)

        # 前后端的校验需要分离：前端检验完，数据到服务器后继续校验，避免黑客绕过客户端发请求
        # 验证是否同意协议
        if not uallow:
            return render(request, 'register.html', {'err_msg': '请同意协议'})
        # 判断数据是否填写完整
        if not all([uname, upwd, cpwd, uemail]):
            return render(request, 'register.html', {'err_msg': '资料请填写完整'})
        # 判断密码是否一致
        # 用户错误提示的数据
        context = {
            'uname': uname,
            'upwd': upwd,
            'cpwd': cpwd,
            'email': uemail,
            'err_msg': '',
            'title': '注册处理'
        }
        if upwd != cpwd:
            context['err_msg'] = '两次输入的密码不一致'
            return render(request, 'register.html', context)
        # 判断用户名是否存在
        if UserInfo.objects.filter(username=uname).count() > 0:
            context['err_msg'] = '用户名已存在'
            return render(request, 'register.html', context)
        # 判断邮箱格式是否正确
        # ^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', uemail):
            context['err_msg'] = '邮箱格式错误'
            return render(request, 'register.html', context)
        # 判断邮箱是否存在
        if UserInfo.objects.filter(email=uemail).count() > 0:
            context['err_msg'] = '邮箱已存在'
            return render(request, 'register.html', context)
        # 处理（创建用户对象）
        user = UserInfo.objects.create_user(uname, upwd, uemail)
        # 稍候进行邮件激发，或许账户不被激活
        user.is_active = False
        user.save()
        # 将账号信息进行加密
        serializer = Serializer(settings.SECRET_KEY, 60 * 60 * 2)
        value = serializer.dumps({'id': user.id})  # 返回bytes
        value = value.decode()  # 转成字符串，用于拼接地址

        # 向用户发送邮件
        msg = '<a href="http://127.0.0.1:8000/user/active/%s">点击激活</a>' % value
        send_mail('天天生鲜账户激活', '', settings.EMAIL_FROM, [uemail], html_message=msg)


        return HttpResponse('请接收邮件激活账户(有效时间两小时)')

def active(request, value):
    pass