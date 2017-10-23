# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import  View
from oms_web.mysql import db_operate
from oms_web import settings
import  os,json,psycopg2,MySQLdb
import datetime
import ansible.runner
from  forms import HostListForm
from models import HostList,SelectHost
from django.views.decorators.csrf import csrf_exempt

# 分页 --应用的库
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import logging
logger = logging.getLogger('django')

# Create your views here.

# def HostManage(request):
# 	return render(request,'hostmanage.html')

def Addip(request):
    if request.method == 'POST':
        print "xxxxxxxxxxxxxx"
        print request.POST
        hostlist_from = HostListForm(request.POST)
        print "----------------"
        print hostlist_from
        if hostlist_from.is_valid():
            hostlist_info = hostlist_from.save(commit=True)
            return HttpResponse('{"recode":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"recode":"fail","msg":"数据保存失败！！"}', content_type='application/json')

class HostManage(View):
    """
    主机列表展示
    """
    def get(self,request):
        hosts=[]
        all_hosts = HostList.objects.all()
        host_nums = all_hosts.count()
        # all_groups = HostList.objects.values('group').distinct().order_by('group')
        host_ip = []
        host_ip = SelectHost.objects.all()
        logger.info(host_ip)
        if host_ip is not None:
            for ip in host_ip:
                logger.info(ip.selectip)
                logger.info(ip.id)
            # 分页
            try:
                page2 = request.GET.get('page' ,1)
            except PageNotAnInteger:
                page2 = 1
            p = Paginator(ip,settings.PAGING,request=request)
            corrects = p.page(page2)
            for correct in corrects.objects.object_list:
                logger.info(correct.id)

        sid_d = request.GET.get('sid',"")
        if sid_d :
            logger.info(type(sid_d))
            logger.info("---------------------------------"+sid_d)
            logger.info(type(int(sid_d)))
            SelectHost.objects.filter(id=sid_d).delete()
            render(request, 'hostmanage.html')

            # sid_d_o = SelectHost.objects.get(id = sid_d)
            # logger.info(sid_d_o )
            #sid_d_o.delete()

        group_name = request.GET.get('gg',"")
        print group_name
        if group_name:
            host_list = all_hosts.filter(group=group_name)
            if host_list is not None:
                for host_lt in host_list:
                    print host_lt.addip
                    hosts.append(host_lt.addip)

        print hosts
        return render(request, 'hostmanage.html',locals(),{
            "hosts":hosts,"host_ip":host_ip
        })

    def post(self,request):
        host = request.POST.getlist('hostaddip', "")
        group = request.GET.get('gg',"")
        print host,group
        # all_groups = HostList.objects.values('group').distinct().order_by('group')

        if host is not None:
            for i in range(len(host)):
                try:
                    print ("序号：%s   值：%s" % (i + 1, host[i]))
                    p = SelectHost(selectip=host[i],selectgroup=group)
                    p.save()
                except Exception as e:
                    print e
                    msg= host[i]+"已经存在"
                    print msg

        return render(request, 'hostmanage.html')

class HostInfo(View):
    def get(self, request):

        print type(request.user.username)
        my_result=''
        ab_config = request.GET.get('ansible_config', "")
        print type(ab_config)
        if ab_config == "22":
            print ab_config
            logger.info("--- 生成ansible的配置文件 ---")
            file = settings.ANSIBLE_ALL_HOST
            file_cmd = 'rm -f ' + file
            os.system(file_cmd)
            logger.info(file_cmd + u"删除原配置文件")
            file_object = open(file, 'w')
            try:
                single_group = HostList.objects.values('group').distinct().order_by('group')
                for gp in single_group:
                    logger.info(gp['group'])
                    file_object.write('[' + gp['group'] + ']\n')
                    hosts = HostList.objects.filter(group=gp['group'])  # 获取主机组的信息
                    for host in hosts:
                        logger.info(host.addip)
                        file_object.write(host.addip + '\n')
                    file_object.write('\n\n')
                my_result = u"ansible配置文件生成成功"
                logger.info("ansible配置文件生成成功")
            except IOError:
                my_result = u"ansible配置文件生成失败"
                logger.info("ansible配置文件生成失败")
            finally:
                file_object.close()

        # 主机信息  分页 顺序
        all_hosts = HostList.objects.order_by("id")
        host_group = request.GET.get('gg', "")
        print host_group
        if host_group:
            allhost = all_hosts.filter(group=host_group)
        else:
            allhost = all_hosts
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(allhost, settings.PAGING, request=request)

        allhost = p.page(page)
        print allhost.object_list

        return render(request, 'hostinfo.html', locals())

        # return render(request, 'hostinfo.html', {"allhost": allhost,
        #                                          "host_group": host_group,
        #                                          "my_result":my_result})

class Hostlogin(View):
    def get(self, request):
        return render(request, 'hostlogin.html')



# def add(request):
#         a = request.GET['a']
#         b = request.GET['b']
#         a = int(a)
#         b = int(b)
#         return HttpResponse(str(a+b))
