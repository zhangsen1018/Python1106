import random
import re
import uuid

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from DB.base_view import BaseVerifyView
from market import set_password
from user.forms import RegisterModelForm, LoginModelForm, MemberModelForm
from user.helps import login, send_sms

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
            request.session['ID'] = user.pk
            request.session['username'] = user.username
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


# 个人资料视图类
class PersonalCenterView(BaseVerifyView):
    def get(self, request):
        # 读取数据,渲染页面
        user_id = request.session.get('ID')
        # username = 17629287226
        user = Users.objects.get(pk=user_id)
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
        user_id = request.session.get('ID')
        user = User.objects.filter(id=user_id)
        # 验证表单参数合法性 用表单来验证
        #  验证通过,先将头像保存到本地static/media下,在将头像地址返回
        #  保存头像

        # 保存提交个人信息
        user.update(my_name=data['my_name'],
                    sex=data['sex'],
                    my_birthday=data['my_birthday'],
                    school=data['school'],
                    my_home=data['my_home'],
                    address=data['address'])
        # return redirect('用户:个人资料')

        # 错误信息提示
        context = {
            'user': user
        }
        return render(request, 'user/member.html', context=context)


# 上传头像
@csrf_exempt
def headimg(request):
    user = User.objects.get(pk=request.session.get("ID"))
    user.head = request.FILES['file']
    user.save()
    return JsonResponse({"status": "ok", "head": str(user.head)})


# 忘记密码视图类
class ForgetPassView(View):
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
            username = login_form.cleaned_data.get('username')
            password = set_password(password)
            # 更新用户密码
            Users.objects.filter(username=username).update(password=password)
            # 操作数据库
            # 返回到登录
            return redirect('用户:忘记密码')
        else:
            # 合成响应
            # 验证不通过,返回注册页面
            # 进入到注册页面
            return render(request, 'user/forgetpassword.html', {'form': login_form})


# 用户验证码初版
# def user_code(request):
#     if request.method == 'POST':
#         sj = request.POST.get('username', '')
#         resj = re.compile('^1[3-9]\d{9}$')
#         re_sj = re.search(resj, sj)
#         if re_sj:
#             codesj = "".join([str(random.randint(0, 9)) for _ in range(4)])
#             # print([str(random.randint(0, 9)) for _ in range(4)])
#             # print(codesj)
#             a = get_redis_connection("default")
#             a.set(sj, codesj)
#             a.expire(sj, 180)
#             __business_id = uuid.uuid1()
#             # 信息
#             params = "{\"code\":\"%s\",\"product\":\" --电商-- \"}" % codesj
#             send_sms(__business_id, sj, "注册验证", "SMS_2245271", params)
#             return JsonResponse({"ok": 1})
#         else:
#             return JsonResponse({'err': 0, "erra": "cw"})
#     else:
#         return JsonResponse({'err': 0, "erra": "请求方式错误"})

# 发送短信验证码

# 发送短信验证码
class SendMsm(View):

    def get(self, request):
        pass

    def post(self, request):
        # 1, 接收参数
        username = request.POST.get('username', '')
        rs = re.search('^1[3-9]\d{9}$', username)
        # 判断参数合法性
        if rs is None:
            return JsonResponse({'error': 1, 'errmsg': '电话号码格式错误!'})
        # 2. 处理数据

        # 模拟,最后接入运营商
        """
            1. 生成随机验证码
            2. 保存验证码 保存到redis中, 存取速度快,并且可以方便的设置有效时间
            3. 接入运营商
        """

        # >>>1. 生成随机验证码字符串
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        print("---随机验证码为==={}---".format(random_code))

        # >>>2. 保存验证码到redis中
        # 获取连接
        r = get_redis_connection()
        # 保存手机号码对应的验证码
        r.set(username, random_code)
        r.expire(username, 60)  # 设置60秒后过期

        # # 首先获取当前手机号码的发送次数
        # key_times = "{}_times".format(username)
        # now_times = r.get(key_times)  # 从redis获取的二进制,需要转换
        # # print(int(now_times))
        # if now_times is None or int(now_times) < 10:
        #     # 保存手机发送验证码的次数, 不能超过10次
        #     r.incr(key_times)
        #     # 设置一个过期时间
        #     r.expire(key_times, 3600)  # 一个小时后再发送
        # else:
        #     # 返回,告知用户发送次数过多
        #     return JsonResponse({"error": 1, "errmsg": "发送次数过多"})

        # >>>3. 接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\" 张森爸爸的小可爱 \"}" % random_code
        # print(params)
        rs = send_sms(__business_id, username, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))

        # 3. 合成响应
        return JsonResponse({'error': 0})
