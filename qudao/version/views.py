# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import  View
import logging
import os
logger = logging.getLogger('django')
logger.info('ytest')
from oms_web import settings
import datetime

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

        self.cmd     = 'python ' + self.script_full_path
        self.cmd_run = self.cmd + self.args

    def get_version_list(self):
        # self.result_str   = os.popen(self.cmd_run).read()
        # self.version_list = self.result_str.split(':')[1].strip().split('\n')[:-1]
        self.version_list = ['20170824', '20170825', '20170826']
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

def script_handler(request, arg):
    group_name = arg.lower()
    print('GET - group_name>>>:', group_name)
    # handler_script = settings.VERSION_chdb_script_file

    if group_name == 'chdb':
        handler_script = settings.VERSION_chdb_script_file
    elif group_name == 'chmap':
        handler_script = settings.VERSION_chmap_script_file
    elif group_name == 'chagent':
        handler_script = settings.VERSION_chagent_script_file
    elif group_name == 'dayend':
        handler_script = settings.VERSION_dayend_script_file
    else:
        handler_script = ''
    return handler_script,group_name

class ChDb(View):
    def get(self, request, arg):
        handler_script, group_name = script_handler(request, arg)
        if handler_script:
            chdb_obj       = VersionControl('0', script_file=handler_script)
            version_list   = chdb_obj.get_version_list()
            return render(request, '%sversion.html' % group_name, locals())
        else:
            return HttpResponse("error code: 404,页面不存在")

    def post(self, request, arg):
        handler_script, group_name = script_handler(request, arg)
        logger.info('POST - arg>>>:{}'.format(group_name))
        import json
        logger.info('request data>:%s' % request.POST)
        logger.info('request file>:%s' % request.FILES)

        roll_choice_vers = request.POST.get("roll_choice_vers", '')
        packge_content   = request.POST.get("packge_content")
        teller_chdb_txt  = settings.VERSION_teller_CHDB_TXT
        start_host       = request.POST.get("start_host", '')
        end_host         = request.POST.get("end_host", '')
        res_obj          = BaseResponse()
        # host_list = settings.'%s'_host % group_name

        # 假如接收到的主机ip不是数字，就把错误信息直接返回个前端
        if not start_host.isdigit() and not end_host.isdigit():
            res_obj.error = "主机地址不是一个数字，请输入有效的数字"
            data = json.dumps(res_obj.__dict__)
            logger.info('返回信息', data)
            return HttpResponse(data)

        host_list = getattr(settings, '{}_host'.format(group_name))
        starttime = datetime.datetime.now()

        if start_host and end_host and start_host <= end_host \
                and int(start_host) in host_list \
                and int(end_host) in host_list:

            if roll_choice_vers:
                    chdb_obj = VersionControl('2',
                                          script_file=handler_script,
                                          action=roll_choice_vers,
                                          start_host=start_host,
                                          end_host=end_host,
                                          )
                    chdb_result_str = chdb_obj.action_func()
                    res_obj.status  = True
                    res_obj.data    = chdb_result_str

            else:
                file_obj = request.FILES.get('v_file_obj', '')
                if file_obj:

                    inp_v_name = file_obj.name
                    logger.info("File Name>>:%s" % inp_v_name)
                    # 开始接收文件，并写入到服务器的指定目录下
                    file_path = os.path.join('static', file_obj.name)  # 组合文件的完整路径，
                                                                       # 第一个参数是路径，
                                                                       # 第二个参数是文件名
                    # new_file_obj = open(file_path, 'wb')fi
                    with open(file_path, 'wb') as new_file_obj:
                        [new_file_obj.write(chunk) for chunk in file_obj.chunks()]


                    chdb_obj = VersionControl('1',
                                              script_file=handler_script,
                                              action=inp_v_name,
                                              start_host=start_host,
                                              end_host=end_host,
                                              )
                    chdb_result_str = chdb_obj.action_func()
                    res_obj.status  = True
                    res_obj.data    = chdb_result_str
                else:
                    res_obj.error   = u"升级未完成，请检查日志"
        else:
            res_obj.error = u"主机参数不完整，请检查主机范围;示例:[1-2]或者[1-1]"
        data = json.dumps(res_obj.__dict__)
        logger.info('返回信息',data)
        return HttpResponse(data)


