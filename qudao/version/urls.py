# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from version.views import *

urlpatterns = [
        # url(r'^(\w+)', ChDb.as_view(), name='ChDb'),
        # url(r'^ChMap/$', ChDb.as_view(), name='group_obj'),
        # url(r'^ChAgent/$', ChDb.as_view(), name='group_obj'),
        url(r'^(\w+)/$', ChDb.as_view(), name='group_obj'),
        # url(r'^DayEnd/$', ChDb.as_view(), name='group_obj'),
]

