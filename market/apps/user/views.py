from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.

# 定义视图类
# 在应用里创建一个加密方法
from market import set_password
from user.forms import RegisterModelForm, LoginModelForm
from user.helps import check_login
from user.models import Users



# 定义一个注册视图类
class RegisterView(View): # 注册 直接定义get 和 post
    template_name = 'user/reg.html'

    def get(self, request):
        # 展示登录表单
        return render(request, self.template_name)

    def post(self, request):
        # 完成用户信息的注册
        # 接收参数
        # 渲染提交的数据
        data = request.POST
        # 验证参数合法性 用表单来验证
        form = RegisterModelForm(data)
        if form.is_valid():
            # 操作数据库
            cleaned_data = form.cleaned_data
            # 创建一个用户
            # 清洗过的数据用get得到
            user = Users()
            user.username = cleaned_data.get('username')
            user.password = set_password(cleaned_data.get('password'))
            user.save()

            return redirect('用户:用户登录')
        else:
            # 错误
            return render(request, self.template_name, context={'form': form})

@check_login
# 定义一个登录视图类
class LoginView(View):  # 登录 直接定义get 和 post
    def get(self, request):
        return render(request, 'user/login.html')

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
            # 返回到登录页
            return redirect('用户:首页')
        else:
            # 合成响应
            # 进入到登录页面
            return render(request, 'user/login.html', {'form': form})

def index(request):
    return render(request, 'user/index.html')