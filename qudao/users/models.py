# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.



class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u"昵称",default="")
    gender    = models.CharField(max_length=5,choices=(("male",u"男"),("female",u"女")),default="male")
    address   = models.CharField(max_length=100,verbose_name=u"地址",default="")
    mobile      = models.CharField(max_length=11, verbose_name=u"手机号",null=True, blank=True)

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username