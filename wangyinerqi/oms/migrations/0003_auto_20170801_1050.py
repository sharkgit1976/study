# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-01 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oms', '0002_ansible_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ansible_result',
            name='asmsg',
            field=models.CharField(default='', max_length=8192, verbose_name='\u9519\u8bef\u4fe1\u606f'),
        ),
    ]