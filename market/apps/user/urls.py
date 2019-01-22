from django.conf.urls import url

from DB.base_view import BaseVerifyView
from user.views import LoginView, RegisterView, index, MemberView, ForgetPassView, PersonalCenterView, SendMsm

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name="用户注册"),
    url(r'^login/$', LoginView.as_view(), name="用户登录"),
    url(r'^index/$', index, name="首页"),
    url(r'^member/$', MemberView.as_view(), name="个人中心"),
    url(r'^PersonalCenter/$', PersonalCenterView.as_view(), name="个人资料"),
    url(r'^forgetpassword/$', ForgetPassView.as_view(), name="忘记密码"),
    # url(r'^code/$', user_code, name="验证码"),
    url(r'^SendMsm/$', SendMsm.as_view(), name="验证码"),



]
