# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from oms.views import *

urlpatterns = [
	url(r'^CmdRun/$',	CmdRun.as_view(),	name='CmdRun'),
	url(r'^dayend/$',  dayend.as_view(),  name='dayend'),
	url(r'^DbManage/$',  DbManage.as_view(),  name='DbManage'),
	url(r'^Pg2Manage/$',  Pg2Manage.as_view(),  name='Pg2Manage'),
	url(r'^AutoDeploy/$',  AutoDeploy.as_view(),  name='AutoDeploy'),
	url(r'^reSelect/$',  reSelect.as_view(),  name='reSelect'),
	url(r'^HostDesc/$',  HostDesc.as_view(),  name='HostDesc'),
]



