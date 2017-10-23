# coding:utf-8 
__author__ = 'zhd'
__date__ = '2017/7/25 23:01'

import  xadmin
from xadmin import views
from .models import HostList

class BaseSetting(object):
    use_bootswatch = True

class GlobalSetting(object):
    site_title = "新晨自动化运维"
    site_footer = "新晨科技股份有限公司"
    menu_style = "accordion"
    #menu_style = "default"


class HostListAdmin(object):
    list_display = ['group','hostname','addip','status']
    search_fields = ['group','hostname','addip','status']
    list_filter = ['group','addip','status']
    show_bookmarks = False
    list_per_page = 8

xadmin.site.register(HostList,HostListAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

