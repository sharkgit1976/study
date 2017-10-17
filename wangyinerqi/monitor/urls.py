# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from monitor.views import *

urlpatterns = [
	url(r'^MonitorRedis/$', MonitorRedis.as_view(), name='MonitorRedis'),
	url(r'^MonitorRedisInfo/$', MonitorRedisInfo.as_view(), name='MonitorRedisInfo'),
	url(r'^Redis_chart/$', Redis_chart.as_view(), name='Redis_chart'),
]
