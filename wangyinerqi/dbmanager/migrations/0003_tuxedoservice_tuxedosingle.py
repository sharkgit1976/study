# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-29 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanager', '0002_auto_20170728_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='TuxedoService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(max_length=20, unique=True, verbose_name='\u670d\u52a1ID\u53f7')),
                ('service_name', models.CharField(blank=True, max_length=30, verbose_name='\u670d\u52a1\u540d\u79f0')),
                ('service_desc', models.TextField(blank=True, default='', verbose_name='\u670d\u52a1\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': 'tuxedo\u670d\u52a1\u5217\u8868',
                'verbose_name_plural': 'tuxedo\u670d\u52a1\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='TuxedoSingle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('single_name', models.CharField(max_length=20, unique=True, verbose_name='\u8fdb\u7a0b\u540d\u79f0')),
                ('single_command', models.CharField(blank=True, max_length=30, verbose_name='\u8fdb\u7a0b\u542f\u52a8\u547d\u4ee4')),
                ('single_desc', models.TextField(blank=True, default='', verbose_name='\u8fdb\u7a0b\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': '\u5355\u4e2a\u8fdb\u7a0b\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u5355\u4e2a\u8fdb\u7a0b\u4fe1\u606f\u8868',
            },
        ),
    ]