# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from dbmanager.views import *

urlpatterns = [
	url(r'^HostManage/$',  HostManage.as_view(),  name='HostManage'),
	url(r'^HostInfo/$',  HostInfo.as_view(),  name='HostInfo'),
	url(r'^Hostlogin/$',  Hostlogin.as_view(),  name='Hostlogin'),
	url(r'^addip/$',       Addip,       name='Addip'),
	# url(r'^select_ip/$',  Select_host,  name='select_ip'),
]



