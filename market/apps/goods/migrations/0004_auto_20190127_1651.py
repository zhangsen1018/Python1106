# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-27 16:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20190127_1447'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityzonegoods',
            options={'verbose_name': '首页活动专区商品列表', 'verbose_name_plural': '首页活动专区商品列表'},
        ),
        migrations.AlterModelTable(
            name='activityzonegoods',
            table='ActivityZoneGoods',
        ),
    ]
