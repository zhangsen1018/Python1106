from datetime import date

from django import forms
from django.core.validators import RegexValidator

from user.models import Users
from market import set_password


# 注册ModelForm的模型类
class RegisterModelForm(forms.ModelForm):
    # 用户手机号
    username = forms.CharField(
        error_messages={
            "required": "手机必填",
        },
        validators=[
            RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
        ]
    )
    # 单独定义一个字段
    # 密码
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })
    # 确认密码
    repassword = forms.CharField(max_length=16,
                                 min_length=8,
                                 error_messages={
                                     'required': '必须填写密码',
                                     'min_length': '密码最小长度必须为8位',
                                     'max_length': '密码最大长度不能超过16位',
                                 })

    # 模型用的 Users
    class Meta:
        model = Users
        fields = ['username']

        # 提示错误信息
        error_messages = {
            "username": {
                'required': '用户名必须填写',
                'max_length': '用户名长度不能大于11',
            }
        }

    # 验证在数据库中 验证手机号是否存在
    def clean_username(self):  # 验证手机号是否已经被注册
        username = self.cleaned_data.get('username')
        flag = Users.objects.filter(username=username).exists()
        if flag:
            # 在数据库中存在 提示错误
            raise forms.ValidationError("该手机号已经被注册,请重新填写")
        else:
            # 返回单个字段 ,不用返回全部
            return username

    # 验证密码是否一致
    def clean(self):
        # 判断两次密码是否一致
        # 在清洗的数据中的到表单提交的数据,密码和确认密码
        # 获取用户名和密码
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')

        if password and repassword and password != repassword:
            # 在密码和确认密码,并且确认密码和密码不一样的时候,提示错误信息
            raise forms.ValidationError({'repassword': "两次密码不一致!"})
            # 将用户信息保存到cleaned_data中
            # 返回清洗后的所有数据
        return self.cleaned_data


# 登录ModelForm的模型类
class LoginModelForm(forms.ModelForm):
    # 用户手机号
    username = forms.CharField(
        error_messages={
            "required": "手机号必填",
        },
        validators=[
            RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
        ]
    )
    # 单独定义一个字段,密码
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })

    # 模型用的 Users
    class Meta:
        model = Users
        # 验证手机号
        fields = ['username', 'password']
        # 提示错误信息
        error_messages = {
            "username": {
                'required': '手机号必须填写',
                'max_length': '手机号长度不能大于11',
            },
            'password': {
                'required': '请填写密码',
            },
        }

    def clean(self):
        # # 验证手机号
        # 从清洗的数据中的得到手机号
        username = self.cleaned_data.get('username')

        try:
            # 如果 清洗的数据中有手机号和数据库的一致
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            # 不一致,提示错误
            raise forms.ValidationError({'username': '手机号错误'})

        # 验证密码
        # 空字符串是因为创建的加密方法需要必须传值
        password = self.cleaned_data.get('password', '')
        # 如果 清洗的数据中有密码和数据库的不一致,提示错误信息
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码错误'})

        # 返回所有清洗后的数据
        self.cleaned_data['user'] = user
        return self.cleaned_data


# 定义个人资料ModelForm的模型
class MemberModelForm(forms.ModelForm):
    # 用户昵称
    my_name = forms.CharField(max_length=50,
                              min_length=2,
                              error_messages={
                                  'min_length': '用户昵称最小长度必须为2位',
                                  'max_length': '用户昵称最大长度不能超过50位',
                              })
    my_birthday = forms.DateField()
    school = forms.CharField(max_length=50,
                             error_messages={
                                 'max_length': '学校最大长度不能超过50位'
                             })
    my_home = forms.CharField(max_length=50,
                              error_messages={
                                  'max_length': '用户详细地址位置最大长度不能超过50位'
                              })
    address = forms.CharField(max_length=50,
                              error_messages={
                                  'max_length': '用户的故乡最大长度不能超过50位'
                              })
    tel = forms.CharField(error_messages={
        "required": "手机号必填",
    },
        validators=[
            RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
        ]
    )

    # 模型用的 Users
    class Meta:
        model = Users
        fields = ['my_name', 'school', 'my_home', 'address', 'tel']
        # 提示错误信息
        error_messages = {
            "my_name": {
                'required': '用户昵称必须填写',
                'max_length': '用户昵称长度不能大于50',
                'min_length': '用户昵称最小长度必须为2位',
            },
            'school': {
                'max_length': '学校最大长度不能超过50位'
            },
            'my_home': {
                'max_length': '用户详细地址位置最大长度不能超过50位'
            },
            'address': {
                'max_length': '用户的故乡最大长度不能超过50位'
            },
            'tel': {
                'required': '手机号必须填写',
                'max_length': '手机号长度不能大于11',
            }
        }
