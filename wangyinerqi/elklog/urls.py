# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from elklog.views import *

urlpatterns = [
        # url(r'^(\w+)', ChDb.as_view(), name='ChDb'),
        url(r'^ELK/$', ChELK.as_view(), name='ELK'),

]

