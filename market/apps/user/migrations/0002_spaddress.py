# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-27 22:21
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False)),
                ('Create_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
                ('hcity', models.CharField(blank=True, max_length=50, null=True, verbose_name='省')),
                ('hproper', models.CharField(blank=True, max_length=50, null=True, verbose_name='市')),
                ('harea', models.CharField(max_length=50, verbose_name='区')),
                ('detail', models.CharField(max_length=255, verbose_name='详细地址')),
                ('username', models.CharField(max_length=100, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}$', '手机号码格式错误')], verbose_name='收货人手机号')),
                ('isDefault', models.BooleanField(default=False, verbose_name='是否为默认地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Users', verbose_name='所属用户')),
            ],
            options={
                'verbose_name': '收货地址管理',
                'verbose_name_plural': '收货地址管理',
                'db_table': 'sp_address',
            },
        ),
    ]
