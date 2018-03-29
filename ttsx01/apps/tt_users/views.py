from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .models import UserInfo, AddressInfo
import re
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from celery_tasks.tasks import send_user_active
# from celery_tasks.tasks import send_active_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_redis import get_redis_connection
from tt_goods.models import GoodsSKU
from utils.views import LoginRequiredView, LoginRequiredViewMixin


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
        user = UserInfo.objects.create_user(uname, uemail, upwd)
        # 稍候进行邮件激发，或许账户不被激活
        user.is_active = False
        user.save()
        # # 将账号信息进行加密
        # serializer = Serializer(settings.SECRET_KEY, 60 * 60 * 2)
        # value = serializer.dumps({'id': user.id})  # 返回bytes
        # value = value.decode()  # 转成字符串，用于拼接地址
        # #
        # # 向用户发送邮件
        # msg = '<a href="http://127.0.0.1:8000/user/active/%s">点击激活</a>' % value
        # send_mail('天天生鲜账户激活', '', settings.EMAIL_FROM, [uemail], html_message=msg)

        # 使用celery发送激活邮件
        send_user_active.delay(user)
        # send_active_email.delay (uemail, uname, value)

        return HttpResponse('请接收邮件激活账户(有效时间两小时)')


def active(request, value):
    serializer = Serializer(settings.SECRET_KEY)
    try:
        # 解析用户编号
        dict = serializer.loads(value)
        userid = dict.get('id')
        # 激活账户
        user = UserInfo.objects.get(pk=userid)
        user.is_active = True
        user.save()
        # 转向登录页面
        return redirect('/user/login')
    except SignatureExpired as e:
        return HttpResponse('Sorry,Your activation link has expired.')


def exists(request):
    '判断用户名或邮箱是否存在'
    uname = request.GET.get('uname')
    if uname is not None:
        result = UserInfo.objects.filter(username=uname).count()
    uemail = request.GET.get('email')
    if uemail is not None:
        result1 = UserInfo.objects.filter(email=uemail).count()
    return JsonResponse({'result': result}, {'result1': result1})


class LoginView(View):
    def get(self, request):
        uname = request.COOKIES.get('uname', '')
        return render(request, 'login.html', {'title': '登录', 'uname': uname})

    def post(self, request):
        # 接收数据
        dict = request.POST
        uname = dict.get('username')
        pwd = dict.get('pwd')
        remember = dict.get('remember')

        # 构造返回值
        context = {
            'title': '登录处理',
            'uname': uname,
            'pwd': pwd,
            'err_msg': '请填写完成信息'
        }

        # 验证是否填写数据
        if not all([uname, pwd]):
            return render(request, 'login.html', context)

        #验证用户名、密码是否正确
        user = authenticate(username=uname, password=pwd)
        if user is None:
            context['err_msg'] = '用户名或密码错误'
            return render(request, 'login.html', context)

        #判断用户是否激活
        if not user.is_active:
            context['err_msg'] = '请到邮箱激活账户'
            render(request, 'login.html', context)

        #记录状态
        login(request, user)

        response = redirect('/user/info')

        #是否记住用户名
        if remember is not None:
            response.set_cookie('uname', uname, expires=60*60*24*7)
        else:
            response.delete_cookie('uname')

        # 转向用户中心
        return response


def logout_user(request):
    # django.contrib.auth提供的退出方法
    logout(request)
    return redirect('/user/login')


@login_required
def info(request):
    # # django验证系统：判断用户是否登录
    # if request.user.is_authenticated():
    #     pass
    # else:
    #     return redirect('/user/login')

    """从redis中读取浏览记录
    浏览记录在商品的详细页视图中添加（后面再做）
    获取redis服务器的连接"""
    client = get_redis_connection('default')
    # history_list = client.lrange('history%d' % request.user.id, 0, -1)  # 获取到的是一个列表
    # history_list2 = []
    # if history_list:
    #     for gid in history_list:
    #         history_list2.append(GoodsSKU.objects.get(pk=gid))
    #
    # # 查询默认收货地址，返回列表，如果不存在则返回空列表
    # addr = request.user.addressinfo_set.all().filter(isDefault=True)
    # if addr:
    #     addr = addr[0]
    # else:
    #     addr = ''
    #
    # context = {
    #     'title': '个人信息',
    #     'addr' : addr,
    #     'history': history_list2,
    # }

    return render(request, 'user_center_info.html')

@login_required
def order(request):
    context = {

    }
    return render(request, 'user_center_order.html', context)


class SiteView(LoginRequiredViewMixin, View):
    def get(self, request):
        # 查询当前用户的收货地址
        addr_list = AddressInfo.objects.filter(user=request.user)
        context = {
            'title': '收货地址',
            'addr_list': addr_list,
        }
        return render(request, 'user_center_site.html', context)


    def post(self, request):
        dict = request.POST

        receiver = dict.get('receiver')
        province = dict.get('province')
        city = dict.get('city')
        district = dict.get('district')
        addr1 = dict.get('addr')
        code = dict.get('code')
        phone = dict.get('phone')
        default = dict.get('default')
