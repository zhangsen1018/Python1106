import random
import re
import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from DB.dxyzm import send_sms

from django.views import View
from django_redis import get_redis_connection

from DB.base_view import BaseVerifyView
from market import set_password
from user.forms import RegisterModelForm, LoginModelForm
from user.helps import login

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
            us = Users.objects.filter(user=user)
            if us:
                password = login_form.cleaned_data.get('password')
                pwd = set_password(password)
                if Users.objects.filter(pwd=pwd):
                    # 操作数据库
                    # 返回到首页
                    return redirect('用户:个人中心')
            else:
                context = {
                    'context': '用户名或者密码错误'
                }
                return render(request, 'user/login.html', context=context)
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
        # 读取数据,渲染页面
        # username=request.session.get('username')
        username = 17629287226
        user = Users.objects.get(username=username)
        context = {
            'user': user
        }
        return render(request, 'user/infor.html', context=context)

    # @method_decorator(check_login)
    def post(self, request):
        # 完成用户信息的注册
        # 接收参数
        # 渲染提交的数据
        data = request.POST
        # 验证表单参数合法性 用表单来验证
        form = RegisterModelForm(data)
        if form.is_valid():
            #  验证通过,先将头像保存到本地static/media下,在将头像地址返回
            #  保存头像
            username = request.POST.get('username')
            # 操作数据库
            # 头像地址
            img = f'media/{tel}.png'
            my_name = form.cleaned_data.get('my_name')
            sex = request.POST.get('sex')
            my_birthday = request.POST.get('my_birthday')
            school = request.POST.get('school')
            my_home = request.POST.get('my_home')
            address = request.POST.get('address')
            # 保存提交个人信息
            Users.objects.filter(username=username).update(my_name=my_name,
                                                           img=img,
                                                           sex=sex,
                                                           my_birthday=my_birthday,
                                                           school=school,
                                                           my_home=my_home,
                                                           address=address)
            return redirect('用户:个人资料')
        else:
                # 错误信息提示
            return render(request, 'user/member.html', context={'form': form})


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
            password = login_form.cleaned_data['password']
            username= login_form.cleaned_data.get('username')
            password = set_password(password)
            # 更新用户密码
            Users.objects.filter(username=username).update(password=password)
            # 操作数据库
            # 返回到登录
            return redirect('用户:登录')
        else:
            # 合成响应
            # 验证不通过,返回注册页面
            # 进入到注册页面
            return render(request, 'user/reg.html', {'form': login_form})


def user_code(request):
    if request.method == 'POST':
        sj = request.POST.get('username', '')
        resj = re.compile('^1[3-9]\d{9}$')
        re_sj = re.search(resj, sj)
        if re_sj:
            codesj = "".join([str(random.randint(0, 9)) for _ in range(4)])
            # print([str(random.randint(0, 9)) for _ in range(4)])
            # print(codesj)
            a = get_redis_connection("default")
            a.set(sj, codesj)
            a.expire(sj, 180)
            __business_id = uuid.uuid1()
            # 信息
            params = "{\"code\":\"%s\",\"product\":\"电商 \"}" % codesj
            send_sms(__business_id, sj, "注册验证", "SMS_2245271", params)
            return JsonResponse({"ok": 1})
        else:
            return JsonResponse({'err': 0, "erra": "cw"})
    else:
        return JsonResponse({'err': 0, "erra": "请求方式错误"})
