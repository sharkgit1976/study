# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import  View
import logging
import os
logger = logging.getLogger('django')
logger.info('ytest')
from oms_web import settings
# Create your views here.


class BaseResponse:
    def __init__(self):
        self.status = False
        self.data = None
        self.error = None


class VersionControl(object):
    def __init__(self,args, script_file='',
                 scritpt_dir=settings.VERSION_script_dir,
                 action='',
                 start_host='',
                 end_host='',
                 ):
        self.args             = ' ' + args
        self.script_file      = script_file
        self.script_dir       = scritpt_dir
        self.action           = ' ' + action
        self.start_host       = ' ' + start_host
        self.end_host         = end_host
        self.script_full_path = self.script_dir + self.script_file

        self.cmd = 'python ' + self.script_full_path
        self.cmd_run = self.cmd + self.args

    def get_version_list(self):
        self.result_str   = os.popen(self.cmd_run).read()
        self.version_list = self.result_str.split(':')[1].strip().split('\n')[:-1]
        self.version_list.reverse()
        return self.version_list

    def action_func(self):
        """
          测试是使用  host_range = 8-8
        :return:
        """
        self.cmd_run = self.cmd_run +  self.action + self.start_host + '-' + self.end_host
        # self.result_str = os.popen(self.cmd_run).read()
        self.result_str = self.cmd_run
        return self.result_str


class ChMap(View):
    def get(self, request):
        return render(request,'chmapversion.html')
class ChAgent(View):
    def get(self, request):

        return render(request,'chagentversion.html')

class ChDb(View):
    def get(self, request):
        logger.info(request.GET)
        group_obj      = 'chdb'
        # logger.info('>>',arg)
        handler_script = settings.VERSION_chdb_script_file

        if group_obj == 'chdb':
            handler_script = settings.VERSION_chdb_script_file
        elif group_obj == 'chmap':
            handler_script = settings.VERSION_chmap_script_file
        chdb_obj       =  VersionControl('0', script_file=handler_script)
        version_list   = chdb_obj.get_version_list()
        return render(request,'%sversion.html' %group_obj,{'version_list':version_list})

    def post(self,request):
        import json
        logger.info(request.POST)

        roll_choice_vers = request.POST.get("roll_choice_vers")
        start_host       = request.POST.get("start_host")
        end_host         = request.POST.get("end_host")
        v_name           = request.POST.get("v_name")
        file_obj         = request.FILES.get('v_file_obj')
        logger.info("File>>",file_obj.name)
        # group_tag        = request.POST.get("group_tag")
        logger.info(request.POST)
        res_obj     = BaseResponse()
        if start_host and end_host and start_host <= end_host \
                and start_host.isdigit() and end_host.isdigit():

            if roll_choice_vers:
                    chdb_obj = VersionControl('2',
                                          script_file=settings.VERSION_chdb_script_file,
                                          action=roll_choice_vers,
                                          start_host=start_host,
                                          end_host=end_host,
                                          )
                    chdb_result_str = chdb_obj.action_func()
                    res_obj.status  = True
                    res_obj.data    = chdb_result_str

            elif v_name:
                chdb_obj = VersionControl('1',
                                          script_file=settings.VERSION_chdb_script_file,
                                          action=v_name,
                                          start_host=start_host,
                                          end_host=end_host,
                                          )
                chdb_result_str = chdb_obj.action_func()

                res_obj.status = True
                res_obj.data = chdb_result_str
            else:
                res_obj.status = False
                res_obj.error = "文件名没写"
        else:
            res_obj.status = False
            res_obj.error = "主机参数不完整，请检查主机范围;示例:[1-2]或者[1-1]"
        data = json.dumps(res_obj.__dict__)
        return HttpResponse(data)


class DayEnd(View):
    def get(self, request):
        return render(request,'dayendversion.html')
