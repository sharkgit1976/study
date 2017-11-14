# coding:utf-8
from django.conf.urls import url
from django.contrib import admin
from version.views import *
from django.conf.urls import (
        handler400,handler403,handler404,handler500
)

# handler400 = 'webadmin.handle_views.bad_request'
# handler403 = 'webadmin.views.permission_denied'
handler404 = 'version.views.page_not_found'
# handler500 = 'webadmin.handle_views.server_error'

urlpatterns = [
        # url(r'^(\w+)', ChDb.as_view(), name='ChDb'),
        # url(r'^ChMap/$', ChDb.as_view(), name='group_obj'),
        # url(r'^ChAgent/$', ChDb.as_view(), name='group_obj'),
        url(r'^(\w+)/$', ChDb.as_view(), name='group_obj'),
        # url(r'^DayEnd/$', ChDb.as_view(), name='group_obj'),
]

