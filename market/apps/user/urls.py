from django.conf.urls import url

from user.views import RegisterView, LoginView, index

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name="用户注册"),
    url(r'^login/$', LoginView.as_view(), name="用户登录"),
    url(r'^index/$',index , name="首页"),
]
