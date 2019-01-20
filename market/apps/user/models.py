from django.core.validators import MinLengthValidator
from django.db import models
from DB.base_model import Base_model


# Create your models here.
class Users(Base_model):
    username = models.CharField(max_length=11,
                                validators=[
                                    MinLengthValidator(11, '手机号至少11位')
                                ],
                                verbose_name='用户名,使用手机号')
    password = models.CharField(max_length=255, verbose_name='密码')
    my_name = models.CharField(max_length=50, blank=True, null=True,
                               validators=[
                                   MinLengthValidator(2, '用户昵称至少2位')
                               ],
                               verbose_name='用户昵称')
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    sex = models.IntegerField(choices=gender_choices, default=1, verbose_name='性别选择,默认男')
    my_birthday = models.DateField(blank=True, null=True, verbose_name='用户生日,默认为空')
    school = models.CharField(max_length=50, blank=True, null=True, verbose_name='学校')
    my_home = models.CharField(max_length=50, blank=True, null=True, verbose_name='用户详细地址位置')
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name='用户的故乡')
    tel = models.CharField(max_length=11, blank=True, null=True, verbose_name='电话号码')
    # 用户头像从setting文件直接找到静态文件的储存路径
    use_img = models.ImageField(upload_to='user_img', default='images/infortx.png', verbose_name='用户头像')

    def __str__(self):
        return self.username

    class Meta:
        db_table = "sp_user"
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name
