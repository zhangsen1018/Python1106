from django.conf.urls import url

from DB.base_view import BaseVerifyView
from user.views import LoginView, RegisterView, index, MemberView, ForgetPassView, PersonalCenterView

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name="用户注册"),
    url(r'^login/$', LoginView.as_view(), name="用户登录"),
    url(r'^index/$', index, name="首页"),
    url(r'^member/$', MemberView.as_view(), name="个人中心"),
    url(r'^PersonalCenter/$', PersonalCenterView.as_view(), name="个人资料"),
    url(r'^forgetpassword/$', ForgetPassView.as_view(), name="忘记密码"),


]
