# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-11 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanager', '0007_redisinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redisinfo',
            name='redis_ip',
            field=models.GenericIPAddressField(null=True, protocol='ipv4'),
        ),
    ]