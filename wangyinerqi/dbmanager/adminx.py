# coding:utf-8 
__author__ = 'zhd'
__date__ = '2017/7/25 23:01'

import  xadmin
from xadmin import views
from .models import *

class BaseSetting(object):
    use_bootswatch = True

class GlobalSetting(object):
    site_title = "新晨自动化运维"
    site_footer = "新晨科技股份有限公司"
    menu_style = "accordion"
    #menu_style = "default"


class HostListAdmin(object):
    list_display = ['group','hostname','addip','status','area']
    search_fields = ['group','hostname','addip','status','area']
    list_filter = ['group','addip','status','area']
    show_bookmarks = False
    list_per_page = 8

class TuxedoServiceAdmin(object):
    list_display = ['service_name','service_group','service_desc']
    search_fields = ['service_name','service_group','service_desc']
    list_filter = ['service_name','service_group','service_desc']
    show_bookmarks = False
    list_per_page = 8

class TuxedoIdAdmin(object):
    list_display = ['service_id','service_name','service_group','service_desc']
    search_fields = ['service_id','service_name','service_group','service_desc']
    list_filter = ['service_id','service_name','service_group','service_desc']
    show_bookmarks = False
    list_per_page = 8

class TuxedoSingleAdmin(object):
    list_display = ['single_name','single_command','single_desc']
    search_fields = ['single_name','single_command','single_desc']
    list_filter =  ['single_name','single_command','single_desc']
    show_bookmarks = False
    list_per_page = 8


class RedisInfoAdmin(object):
    list_display = ['redis_ip','redis_name','redis_port']
    search_fields = ['redis_ip','redis_name','redis_port']
    list_filter =  ['redis_ip','redis_name','redis_port']
    show_bookmarks = False
    list_per_page = 8

xadmin.site.register(HostList,HostListAdmin)
xadmin.site.register(TuxedoService,TuxedoServiceAdmin)
xadmin.site.register(TuxedoId,TuxedoIdAdmin)
xadmin.site.register(RedisInfo,RedisInfoAdmin)
xadmin.site.register(TuxedoSingle,TuxedoSingleAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

