from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

# 在应用里创建一个加密方法
from django.utils.decorators import method_decorator
from django.views import View

from DB.base_view import BaseVerifyView
from market import set_password
from user.forms import RegisterModelForm, LoginModelForm
from user.helps import check_login, check_login_view
from user.models import Users


# 定义一个注册视图类
class RegisterView(View):  # 注册 直接定义get 和 post
    template_name = 'user/reg.html'

    def get(self, request):
        # 展示登录表单
        return render(request, self.template_name)

    def post(self, request):
        # 完成用户信息的注册
        # 接收参数
        # 渲染提交的数据
        data = request.POST
        # 验证表单参数合法性 用表单来验证
        form = RegisterModelForm(data)
        if form.is_valid():
            # 操作数据库
            cleaned_data = form.cleaned_data
            # 创建一个注册用户
            # 得到清洗过的数据
            user = Users()
            user.username = cleaned_data.get('username')
            user.password = set_password(cleaned_data.get('password'))
            user.save()
            return redirect('用户:用户登录')
        else:
            # 错误信息提示
            return render(request, self.template_name, context={'form': form})


# 定义一个登录视图类
class LoginView(View):  # 登录 直接定义get 和 post
    # @check_login_view
    def get(self, request):
        return render(request, 'user/login.html')

    # @check_login_view
    def post(self, request):
        # 接收参数
        data = request.POST
        # 验证数据的合法性
        form = LoginModelForm(data)
        if form.is_valid():
            # 验证成功
            # 数据合法
            # 从session中得到数据
            user = form.cleaned_data.get('user')
            request.session['ID'] = user.pk
            request.session['username'] = user.username
            # 操作数据库
            # 返回到首页
            return redirect('用户:个人中心')
        else:
            # 合成响应
            # 进入到登录页面
            return render(request, 'user/login.html', {'form': form})

    # @method_decorator(check_login)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


def index(request):  # 首页
    return render(request, 'user/index.html')


@check_login
def PersonalCenter(request):  # 个人中心
    return render(request, 'user/infor.html')
