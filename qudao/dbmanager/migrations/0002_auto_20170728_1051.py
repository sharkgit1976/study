# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-28 02:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hostlist',
            options={'verbose_name': '\u4e3b\u673a\u7ba1\u7406\u8868', 'verbose_name_plural': '\u4e3b\u673a\u7ba1\u7406\u8868'},
        ),
        migrations.AddField(
            model_name='hostlist',
            name='add_time',
            field=models.DateField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='hostlist',
            name='cpu',
            field=models.IntegerField(choices=[(1, '8 \u6838'), (2, '16\u6838'), (3, '32\u6838')], default=2, verbose_name='CPU\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='hostlist',
            name='hostname',
            field=models.CharField(default='', max_length=20, verbose_name='\u4e3b\u673a\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='hostlist',
            name='memory',
            field=models.IntegerField(choices=[(1, '16G'), (2, '32G'), (3, '64G')], default=2, verbose_name='\u5185\u5b58\u7c7b\u578b'),
        ),
        migrations.AlterField(
            model_name='hostlist',
            name='group',
            field=models.CharField(choices=[('chmap', '\u8054\u673a\u670d\u52a1'), ('chredis', 'REDIS\u670d\u52a1'), ('chdb', '\u6570\u636e\u4ee3\u7406'), ('chelk', 'EKL\u670d\u52a1'), ('chmq', '\u4e2d\u95f4\u4ef6\u670d\u52a1')], default='chmap', max_length=20, verbose_name='\u4e3b\u673a\u7ec4'),
        ),
        migrations.AlterField(
            model_name='hostlist',
            name='status',
            field=models.IntegerField(choices=[(0, '\u6b63\u5e38\u8fd0\u884c'), (1, '\u6545\u969c\u5904\u7406\u4e2d'), (2, '\u5173\u673a')], default=0, verbose_name='\u72b6\u6001\u7c7b\u578b'),
        ),
    ]
