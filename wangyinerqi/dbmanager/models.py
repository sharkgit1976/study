#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class HostList(models.Model):
	group = models.CharField(max_length=20,choices=(("chmap", u"联机服务"), ("chredis", u"REDIS服务"), ("chdb", u"数据代理"),("chelk", u"EKL服务"),("chmq", u"中间件服务")), verbose_name=u"主机组",default="chmap")
	hostname = models.CharField(max_length=20, verbose_name=u"主机名称",default="")
	cpu = models.IntegerField(choices=((1,u"8 核"),(2,u"16核"),(3,u"32核")),verbose_name=u"CPU类型",default=2)
	memory = models.IntegerField(choices=((1, u"16G"), (2, u"32G"), (3, u"64G")), verbose_name=u"内存类型",default=2)
	addip = models.CharField(max_length=20,verbose_name=u"主机ip",unique=True)
	area = models.IntegerField(choices=((1, u"亦庄"), (2, u"丰台")), verbose_name=u"所属地区", default=1)
	status = models.IntegerField(choices=((0, u"正常运行"), (1, u"故障处理中"), (2, u"关机")), verbose_name=u"状态类型",default=0)
	add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = u"主机管理表"
		verbose_name_plural = verbose_name

class SelectHost(models.Model):
	selectip = models.CharField(max_length=20,verbose_name=u"选择IP",unique=True)
	selectgroup = models.CharField(max_length=20, verbose_name=u"选择主机组",default="")

	class Meta:
		verbose_name = u"选择主机表"

class TuxedoService(models.Model):
	service_name = models.CharField(max_length=30, verbose_name=u"服务名称",blank=True)
	service_group = models.CharField(max_length=20, choices=(
	("chmap", u"联机服务"), ("chcom", u"数据代理"),("chdb", u"数据处理")),
							 verbose_name=u"主机组", default="chmap")
	service_desc = models.TextField(blank=True,verbose_name=u"服务描述", default="")

	class Meta:
		verbose_name = u"tuxedo服务名列表"
		verbose_name_plural = verbose_name

class TuxedoId(models.Model):
	service_id = models.CharField(max_length=30, verbose_name=u"ID号",blank=True)
	service_name = models.CharField(max_length=30, verbose_name=u"服务名称", blank=True)
	service_group = models.CharField(max_length=20, choices=(
		("chmap", u"联机服务"), ("chcom", u"数据代理"), ("chdb", u"数据处理")),
							 verbose_name=u"主机组", default="chmap")
	service_desc = models.TextField(blank=True,verbose_name=u"服务描述", default="")

	class Meta:
		verbose_name = u"tuxedo服务ID列表"
		verbose_name_plural = verbose_name

class TuxedoSingle(models.Model):
	single_group = models.CharField(max_length=20, choices=(
                ("chmap", u"联机服务"), ("chcom", u"数据代理"), ("chdb", u"数据处理")),
                                            verbose_name=u"主机组", default="chmap")
	single_name    = models.CharField(max_length=20,verbose_name=u"进程名称",blank=True)
	single_command = models.CharField(max_length=30, verbose_name=u"进程启动命令",blank=True)
	single_desc = models.TextField(blank=True,verbose_name=u"进程描述", default="")

	class Meta:
		verbose_name = u"单个进程信息表"
		verbose_name_plural = verbose_name


class RedisInfo(models.Model):
	redis_ip      = models.GenericIPAddressField(protocol="ipv4",null=True)
	redis_name    = models.CharField(max_length=20,verbose_name=u"redis名称",blank=True)
	redis_port    = models.CharField(max_length=20,verbose_name=u"redis 端口", blank=True)
	redis_desc    = models.TextField(blank=True, verbose_name=u"redis 功能描述", default="")

	class Meta:
		verbose_name = u"REDIS信息表"
		verbose_name_plural = verbose_name

