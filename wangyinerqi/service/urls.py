# coding:utf-8
from django.conf.urls import url
from service.views import *

urlpatterns = [
	url(r'^ServiceStart/$', ServiceStart.as_view() , name='ServiceStart'),
    url(r'^Servcietuxedo/$', Servcietuxedo.as_view() , name='Servcietuxedo'),
    url(r'^Servicesingle/$', Servicesingle.as_view() , name='Servicesingle'),
    url(r'^ansible_config/$', ansible_config , name='ansible_config'),
    url(r'^tuxedomold/$', tuxedomold , name='tuxedomold'),

]
