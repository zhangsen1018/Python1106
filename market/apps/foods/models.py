from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
from DB.base_model import Base_model


class FoodsSKU(Base_model):
    foods_name = models.CharField(max_length=50,
                                  validators=[
                                      MinLengthValidator(5, '商品名字不能小于5个字符')
                                  ],
                                  verbose_name='商品名字')
    foods_introduce = models.TextField(max_length=200,
                                       validators=[
                                           MinLengthValidator(5, '商品简介不能小于5个字符')
                                       ],
                                       verbose_name='商品简介')
    foods_price = models.CharField(max_length=50,
                                   verbose_name='商品价格')
