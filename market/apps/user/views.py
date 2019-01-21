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
from user.helps import login, check_login

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
        login_form = LoginModelForm(data)
        if login_form.is_valid():
            # 验证成功
            # 数据合法
            # 从session中得到数据
            # 单独创建方法保存session,更新资料
            user = login_form.cleaned_data.get('user')
            # request.session['ID'] = user.pk
            # request.session['username'] = user.username
            login(request, user)
            # 操作数据库
            # 返回到首页
            return redirect('用户:个人中心')
        else:
            # 合成响应
            # 进入到登录页面
            return render(request, 'user/login.html', {'form': login_form})

    # @method_decorator(check_login)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


def index(request):  # 首页
    return render(request, 'user/index.html')


# 定义个人中心类视图
class MemberView(BaseVerifyView):  # 个人中心视图类
    # @method_decorator(check_login)
    def get(self, request):
        return render(request, 'user/member.html')

    # @method_decorator(check_login)
    def post(self, request):
        pass


class PersonalCenterView(BaseVerifyView):  # 个人资料视图类
    def get(self, request):
        return render(request, 'user/infor.html')

    # @method_decorator(check_login)
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
            user.my_name = cleaned_data.get('my_name')
            user.school = set_password(cleaned_data.get('school'))
            user.my_home = set_password(cleaned_data.get('my_home'))
            user.address = set_password(cleaned_data.get('address'))
            user.tel = set_password(cleaned_data.get('tel'))
            user.save()
            return redirect('用户:个人资料')
        else:
            # 错误信息提示
            return render(request, 'user/infor.html', context={'form': form})


class ForgetPassView(BaseVerifyView):  # 忘记密码视图类
    def get(self, request):
        return render(request, 'user/forgetpassword.html')

    def post(self, request):
        # 接收参数
        data = request.POST
        # 验证数据的合法性
        login_form = LoginModelForm(data)
        if login_form.is_valid():
            # 验证成功
            # 数据合法
            # 从session中得到数据
            # 单独创建方法保存session,更新资料
            user = login_form.cleaned_data.get('user')
            # request.session['ID'] = user.pk
            # request.session['username'] = user.username
            login(request, user)
            # 操作数据库
            # 返回到登录
            return redirect('用户:用户登录')
        else:
            # 合成响应
            # 进入到忘记密码页面
            return render(request, 'user/forgetpassword.html', {'form': login_form})

