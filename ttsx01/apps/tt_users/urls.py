from . import views
from django.conf.urls import url

urlpatterns = [
    # 视图函数：注册
    # url('^register$', views.register),
    # 类视图函数：注册
    url('^register$', views.RegisterView.as_view()),
    url('^active/(.+)$', views.active),
    url('^exists$', views.exists),
    url('^login$', views.login),
    url('^logout$', views.logout),
]