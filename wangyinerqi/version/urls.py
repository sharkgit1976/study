# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from version.views import *

urlpatterns = [
        # url(r'^(\w+)', ChDb.as_view(), name='ChDb'),
        url(r'^ChMap/$', ChMap.as_view(), name='ChMap'),
        url(r'^ChAgent/$', ChAgent.as_view(), name='ChAgent'),
        url(r'^TrunkChDb/$', TrunkChDb.as_view(), name='TrunkChDb'),
        url(r'^ChCom/$', ChCom.as_view(), name='ChCom'),
        url(r'^TellerChDb/$', TellerChDb.as_view(), name='TellerChDb'),
        # url(r'^update_file/$', update_file.as_view(), name='update_file'),
]

