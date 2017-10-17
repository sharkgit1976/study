# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-05 02:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanager', '0004_hostlist_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='TuxedoId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(blank=True, max_length=30, verbose_name='ID\u53f7')),
                ('service_name', models.CharField(blank=True, max_length=30, verbose_name='\u670d\u52a1\u540d\u79f0')),
                ('service_group', models.CharField(choices=[('chmap', '\u8054\u673a\u670d\u52a1'), ('chcom', '\u6570\u636e\u4ee3\u7406'), ('chdb', '\u6570\u636e\u5904\u7406')], default='chmap', max_length=20, verbose_name='\u4e3b\u673a\u7ec4')),
                ('service_desc', models.TextField(blank=True, default='', verbose_name='\u670d\u52a1\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': 'tuxedo\u670d\u52a1ID\u5217\u8868',
                'verbose_name_plural': 'tuxedo\u670d\u52a1ID\u5217\u8868',
            },
        ),
        migrations.AlterModelOptions(
            name='tuxedoservice',
            options={'verbose_name': 'tuxedo\u670d\u52a1\u540d\u5217\u8868', 'verbose_name_plural': 'tuxedo\u670d\u52a1\u540d\u5217\u8868'},
        ),
        migrations.RemoveField(
            model_name='tuxedoservice',
            name='service_id',
        ),
        migrations.AddField(
            model_name='tuxedoservice',
            name='service_group',
            field=models.CharField(choices=[('chmap', '\u8054\u673a\u670d\u52a1'), ('chcom', '\u6570\u636e\u4ee3\u7406'), ('chdb', '\u6570\u636e\u5904\u7406')], default='chmap', max_length=20, verbose_name='\u4e3b\u673a\u7ec4'),
        ),
    ]
