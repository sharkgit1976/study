# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    def __unicode__(self):
            return self.name


class ansible_result(models.Model):
    hostip = models.CharField(max_length=20, verbose_name=u"主机ip", unique=True)
    asmsg= models.CharField(max_length=8192, verbose_name=u"错误信息", default="")
    status = models.CharField(max_length=2,verbose_name=u"消息类型", default="")

    class Meta:
        verbose_name = u"ansible输出信息表"
        verbose_name_plural = verbose_name
