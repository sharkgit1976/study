"""oms_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from oms.views import *
from dbmanager.views import *
from users.views import *
from version.views import *
import xadmin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', Login.as_view(), name='Login'),
    url(r'^index/$', index, name='index'),
    url(r'^remote_exec/$', remote_exec, name='remote_exec'),
#    url(r'^HostManage/$',  HostManage,  name='HostManage'),
#     url(r'^addip/$',       Addip,       name='Addip'),
    # url(r'^cmdrun/$',      cmdrun.as_view(),      name='cmdrun'),
    # url(r'^dayend/$',      dayend,      name='dayend'),
    # url(r'^dbmanage/$',    dbmanage,    name='dbmanage'),
    # url(r'^pg2manage/$',    pg2manage,    name='pg2manage'),
    # url(r'^autodeploy/$',  Autodeploy.as_view(),  name='autodeploy'),
    # url(r'^add/$',         add,         name='add'),
    url(r'^oms/', include('oms.urls', namespace='oms')),
    url(r'^dbm/', include('dbmanager.urls', namespace="dbm")),
    url(r'^elklog/', include('elklog.urls', namespace="elk")),
    url(r'^version/', include('version.urls', namespace="version")),
    url(r'^service/', include('service.urls', namespace="service")),
    url(r'^monitor/', include('monitor.urls', namespace="monitor"))
]
