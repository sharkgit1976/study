# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
import logging
import os, json
import datetime

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
    def __init__(self, args, script_file='',
                 scritpt_dir=settings.VERSION_script_dir,
                 action='',
                 start_host='',
                 end_host='',
                 ):
        self.args = ' ' + args
        self.script_file = script_file
        self.script_dir = scritpt_dir
        self.action = ' ' + action
        self.start_host = ' ' + start_host
        self.end_host = end_host
        self.script_full_path = self.script_dir + self.script_file

        self.cmd = 'python ' + self.script_full_path
        self.cmd_run = self.cmd + self.args

    def get_version_list(self):
        self.result_str = os.popen(self.cmd_run).read()
        logger.info(self.result_str.split(':'))
        self.version_list = self.result_str.split(':')[1].strip().split('\n')
        self.version_list.reverse()
        return self.version_list

    def action_func(self):
        """
          测试是使用  host_range = 8-8
        :return:
        """
        self.cmd_run = self.cmd_run + self.action + self.start_host + '-' + self.end_host
        self.result_str = self.cmd_run
        return self.result_str


class ChMap(View):
    def get(self, request):
        logger.info(request.GET)
        logger.info("------------------------------")
        handler_script = settings.VERSION_chmap_script
        chmap_obj = VersionControl('0', script_file=handler_script)
        logger.info(chmap_obj)
        version_list = chmap_obj.get_version_list()
        logger.info("------chmap----------")
        return render(request, 'chmapversion.html', {'version_list': version_list})

    def post(self, request):
        logger.info(request.POST)
        logger.info(request.FILES)
        roll_choice_vers = request.POST.get("roll_choice_vers")
        start_host = request.POST.get("start_host")
        end_host = request.POST.get("end_host")
        myFile = request.FILES.get('v_file_obj', None)
        packge_content = request.POST.get("packge_content")
        chmap_txt = settings.VERSION_CHMAP_TXT
        logger.info(packge_content)
        logger.info(myFile)
        res_obj = BaseResponse()

        # 拼接python升级回滚的命令
        starttime = datetime.datetime.now()
        # if start_host and end_host and start_host<= end_host \
        #         and start_host.isdigit() and end_host.isdigit():
        if start_host and end_host and start_host <= end_host \
                and int(start_host) in settings.chmap_host and int(end_host) in settings.chmap_host:
            endtime = datetime.datetime.now()
            logger.info((endtime - starttime).seconds)
            # 版本回滚
            if roll_choice_vers:
                starttime = datetime.datetime.now()
                chmap_obj = VersionControl('2', script_file=settings.VERSION_chmap_script,
                                           action=roll_choice_vers,
                                           start_host=start_host,
                                           end_host=end_host)
                chmap_result_str = chmap_obj.action_func()
                logger.info("--------chmap 开始回滚 -------------")
                logger.info(chmap_result_str)
                res_obj.status = True
                res_obj.data = chmap_result_str
                endtime = datetime.datetime.now()
                logger.info((endtime - starttime).seconds)
                # 执行python命令
                logger.info('开始回滚：' + chmap_result_str)
                result_chmap = os.popen(chmap_result_str).read()
                res_obj.data = result_chmap
                # res_obj.data = chmap_result_str

            elif myFile:
                # 上传文件
                logger.info("--------chmap 开始升级-------------")
                if not myFile:
                    res_obj.status = False
                    res_obj.error = "升级包没有上传成功"
                    return HttpResponse(res_obj.__dict__)

                # 打开特定的文件进行二进制的写操作
                destination = open(os.path.join(settings.VERSINO_CHMAP_SOURCE, myFile.name), 'wb+')
                for chunk in myFile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

                chmap_obj = VersionControl('1',
                                           script_file=settings.VERSION_chmap_script,
                                           action=myFile.name,
                                           start_host=start_host,
                                           end_host=end_host,
                                           )
                chmap_result_str = chmap_obj.action_func()
                logger.info("-----------------")
                logger.info(chmap_result_str)
                res_obj.status = True
                res_obj.data = chmap_result_str

                # 打包内容写入
                logger.info("-------------打包内容写入开始-------------")
                package_index = open(chmap_txt, 'a+')
                package_index.write('\n升级内容：' + packge_content)
                package_index.close()
                logger.info('\n升级包名：' + chmap_obj.action)
                logger.info('\n打包时间：' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                logger.info("-------------打包内容写入结束-------------")

                # 执行 Python 命令
                logger.info('开始升级:' + chmap_result_str)
                result_chmap = os.popen(chmap_result_str).read()
                res_obj.data = result_chmap
            else:
                res_obj.status = False
                res_obj.error = "文件名没写"
        else:
            res_obj.status = False
            res_obj.error = "主机参数不完整，请输入正确主机范围(范围:22-23)."
        logger.info('-------chmap执行结束------------')
        logger.info(res_obj.__dict__)

        return HttpResponse(json.dumps(res_obj.__dict__))


class ChAgent(View):
    def get(self, request):
        logger.info(request.GET)
        logger.info("------------------------------")
        handler_script = settings.VERSION_chagent_script
        chagent_obj = VersionControl('0', script_file=handler_script)
        logger.info(chagent_obj)
        logger.info("------------chagent-------")
        version_list = chagent_obj.get_version_list()
        logger.info("------chagent----------")
        return render(request, 'chagentversion.html', {'version_list': version_list})

    def post(self, request):
        logger.info("-----------------ssss-")
        logger.info(request.POST)
        logger.info(request.FILES)
        logger.info("------------------")
        roll_choice_vers = request.POST.get("roll_choice_vers")
        start_host = request.POST.get("start_host")
        end_host = request.POST.get("end_host")
        myFile = request.FILES.get('v_file_obj', None)
        packge_content = request.POST.get("packge_content")
        chagent_txt = settings.VERSION_CHAGENT_TXT
        logger.info(packge_content)
        logger.info(myFile)
        res_obj = BaseResponse()

        # 拼接python升级回滚的命令
        starttime = datetime.datetime.now()
        if start_host and end_host and start_host <= end_host \
                and start_host.isdigit() and end_host.isdigit():
            endtime = datetime.datetime.now()
            logger.info((endtime - starttime).seconds)
            # 版本回滚
            if roll_choice_vers:
                starttime = datetime.datetime.now()
                chagent_obj = VersionControl('2', script_file=settings.VERSION_chagent_script,
                                             action=roll_choice_vers,
                                             start_host=start_host,
                                             end_host=end_host)
                chagent_result_str = chagent_obj.action_func()
                logger.info("--------chagent 开始回滚 -------------")
                logger.info(chagent_result_str)
                res_obj.status = True
                res_obj.data = chagent_result_str
                endtime = datetime.datetime.now()
                logger.info((endtime - starttime).seconds)
                # 执行python命令
                logger.info('开始回滚：' + chagent_result_str)
                # result_chagent = os.popen(chagent_result_str).read()
                # res_obj.data = result_chagent
                res_obj.data = chagent_result_str
                logger.info("---------chagent_result_str-------------")
                logger.info(chagent_result_str)

            elif myFile:
                # 上传文件
                logger.info("--------chagent 开始升级-------------")
                if not myFile:
                    res_obj.status = False
                    res_obj.error = "升级包没有上传成功"
                    return HttpResponse(res_obj.__dict__)

                # 打开特定的文件进行二进制的写操作
                destination = open(os.path.join(settings.VERSINO_CHAGENT_SOURCE, myFile.name), 'wb+')
                for chunk in myFile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

                chagent_obj = VersionControl('1',
                                             script_file=settings.VERSION_chagent_script,
                                             action=myFile.name,
                                             start_host=start_host,
                                             end_host=end_host,
                                             )
                chagent_result_str = chagent_obj.action_func()
                logger.info("-----------------")
                logger.info(chagent_result_str)
                res_obj.status = True
                res_obj.data = chagent_result_str

                # 打包内容写入
                logger.info("-------------打包内容写入开始-------------")
                package_index = open(chagent_txt, 'a+')
                package_index.write('\n升级内容：' + packge_content)
                package_index.close()
                logger.info('\n升级包名：' + chagent_obj.action)
                logger.info('\n打包时间：' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                logger.info("-------------打包内容写入结束-------------")

                # 执行 Python 命令
                logger.info('开始升级:' + chagent_result_str)
                result_chagent = os.popen(chagent_result_str).read()
                res_obj.data = result_chagent
            else:
                res_obj.status = False
                res_obj.error = "文件名没写"
        else:
            res_obj.status = False
            res_obj.error = "主机参数不完整，请加没插主机范围。示例：【1-2】或者【1-1】"
        logger.info('-------chagent执行结束------------')
        logger.info(res_obj.__dict__)

        return HttpResponse(json.dumps(res_obj.__dict__))


class TellerChDb(View):
    def get(self, request):
        logger.info(request.GET)
        group_obj = 'tellerchdb'
        # logger.info('>>',arg)
        handler_script = settings.VERSION_teller_chdb_script

        # if group_obj == 'chdb':
        #     handler_script = settings.VERSION_teller_chdb_script
        # elif group_obj == 'chmap':
        #     handler_script = settings.VERSION_chmap_script
        chdb_obj = VersionControl('0', script_file=handler_script)
        version_list = chdb_obj.get_version_list()
        return render(request, '%sversion.html' % group_obj, {'version_list': version_list})

    def post(self, request):
        logger.info(request.POST)
        logger.info(request.FILES)
        roll_choice_vers = request.POST.get("roll_choice_vers")
        start_host = request.POST.get("start_host")
        end_host = request.POST.get("end_host")
        myFile = request.FILES.get('v_file_obj', None)
        packge_content = request.POST.get("packge_content")
        teller_chdb_txt = settings.VERSION_teller_CHDB_TXT
        logger.info(packge_content)
        logger.info('xxxxxxxxxxx---------xxxxxxxxxxx')
        res_obj = BaseResponse()

        # 拼接 python 升级回滚的命令
        starttime = datetime.datetime.now()
        if start_host and end_host and start_host <= end_host \
                and start_host.isdigit() and end_host.isdigit():
            endtime = datetime.datetime.now()
            logger.info((endtime - starttime).seconds)
            if roll_choice_vers:
                starttime = datetime.datetime.now()
                chdb_obj = VersionControl('2',
                                          script_file=settings.VERSION_teller_chdb_script,
                                          action=roll_choice_vers,
                                          start_host=start_host,
                                          end_host=end_host,
                                          )

                chdb_result_str = chdb_obj.action_func()

                logger.info("-----------------")
                logger.info(chdb_result_str)
                res_obj.status = True
                res_obj.data = chdb_result_str
                endtime = datetime.datetime.now()
                logger.info((endtime - starttime).seconds)

                # 执行 Python 命令
                logger.info('开始回滚:' + chdb_result_str)
                # result_chdb = os.popen(chdb_result_str).read()
                # res_obj.data = result_chdb
                res_obj.data = chdb_result_str

            elif myFile:
                # 上传文件
                if not myFile:
                    res_obj.status = False
                    res_obj.error = "升级包没有上传成功"
                    return HttpResponse(res_obj.__dict__)

                # 打开特定的文件进行二进制的写操作
                destination = open(os.path.join(settings.VERSINO_teller_CHDB_SOURCE, myFile.name), 'wb+')
                for chunk in myFile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

                chdb_obj = VersionControl('1',
                                          script_file=settings.VERSION_teller_chdb_script,
                                          action=myFile.name,
                                          start_host=start_host,
                                          end_host=end_host,
                                          )
                logger.info(chdb_obj)
                chdb_result_str = chdb_obj.action_func()
                logger.info("-----------------")
                logger.info(chdb_result_str)
                res_obj.status = True
                res_obj.data = chdb_result_str

                # 打包内容写入
                logger.info("-------------打包内容写入开始-------------")
                package_index = open(teller_chdb_txt, 'a+')
                package_index.write('\n升级内容：' + packge_content)
                package_index.close()
                logger.info('\n升级包名：' + chdb_obj.action)
                logger.info('\n打包时间：' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                logger.info("-------------打包内容写入结束-------------")

                # 执行 Python 命令
                logger.info('开始升级:' + chdb_result_str)
                # result_chdb = os.popen(chdb_result_str).read()
                # res_obj.data = result_chdb

            else:
                res_obj.status = False
                res_obj.error = "文件名没写"


        else:
            res_obj.status = False
            res_obj.error = "主机参数不完整，请检查主机范围;示例:[1-2]或者[1-1]"

        logger.info('xxxxxxxxxxxxxxxxxxxxxx')

        return HttpResponse(json.dumps(res_obj.__dict__))


class ChCom(View):
    def get(self, request):
        logger.info(request.GET)
        logger.info("----------------------------")
        handler_script = settings.VERSION_chcom_script
        chcom_obj = VersionControl('0', script_file=handler_script)
        logger.info(chcom_obj)
        version_list = chcom_obj.get_version_list()
        logger.info("-------------chcom-----------")
        return render(request, 'chcomversion.html', {'version_list': version_list})

    def post(self, request):
        logger.info(request.POST)
        logger.info(request.FILES)
        roll_choice_vers = request.POST.get("roll_choice_vers")
        start_host = request.POST.get("start_host")
        end_host = request.POST.get("end_host")
        myfile = request.FILES.get('v_file_obj', None)
        packge_content = request.POST.get("packge_content")
        chcom_txt = settings.VERSION_CHCOM_TXT
        logger.info(packge_content)
        logger.info("xxxxxxxxxxx----------xxxxx")
        res_obj = BaseResponse()

        # 拼接python升级回滚的命令
        starttime = datetime.datetime.now()
        if start_host and end_host and start_host <= end_host and start_host.isdigit() and end_host.isdigit():
            endtime = datetime.datetime.now()
            logger.info((endtime - starttime).seconds)
            # 版本回滚
            if roll_choice_vers:
                starttime = datetime.datetime.now()
                chcom_obj = VersionControl('2',
                                           script_file=settings.VERSION_chcom_script,
                                           action=roll_choice_vers,
                                           start_host=start_host,
                                           end_host=end_host,
                                           )
                chcom_result_str = chcom_obj.action_func()
                logger.info("-------------chcom开始回滚----------------")
                logger.info(chcom_result_str)
                res_obj.status = True
                res_obj.data = chcom_result_str
                endtime = datetime.datetime.now()
                logger.info((endtime - starttime).seconds)
                # 执行python命令
                logger.info('开始回滚：' + chcom_result_str)
                result_chcom = os.popen(chcom_result_str).read()
                res_obj.data = result_chcom

            elif myfile and packge_content:
                # 上传文件
                logger.info("------------------chcom开始升级-------------------")
                if not myfile:
                    res_obj.status = False
                    res_obj.error = "升级包没有上传成功"
                    rerurn
                    HttpResponse(res_obj.__dict__)

                # 打开特定的文件进行二进制的写操作
                destination = open(os.path.join("/app/ansible/oms_web/file/", myfile.name), 'wb+')
                for chunk in myfile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()
                logger.info("-------------上传文件结束-------------")
                chcom_obj = VersionControl('1',
                                           script_file=settings.VERSION_chcom_script,
                                           action=myfile.name,
                                           start_host=start_host,
                                           end_host=end_host,
                                           )
                logger.info(chcom_obj)
                chcom_result_str = chcom_obj.action_func()
                logger.info("------------------------------")
                logger.info(chcom_result_str)
                res_obj.status = True
                res_obj.data = chcom_result_str

                # 打包内容写入
                logger.info("-------------打包内容写入开始-------------")
                package_index = open(chcom_txt, 'a+')
                package_index.write('\n升级内容：' + packge_content)
                package_index.close()
                logger.info('\n升级包名：' + chcom_obj.action)
                logger.info('\n打包时间：' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                logger.info("-------------打包内容写入结束-------------")

                # 执行python命令
                logger.info('开始升级' + chcom_result_str)
                result_chcom = os.popen(chcom_result_str).read()
                res_obj.data = result_chcom

            else:
                res_obj.status = False
                res_obj.error = "文件名没写"
        else:
            res_obj.status = False
            res_obj.error = "主机参数不完整，请输入正确的主机范围（范围：22-23）."
        logger.info('---------------chcom执行结束------------------')
        logger.info(res_obj.__dict__)

        return HttpResponse(json.dumps(res_obj.__dict__))

        # class DayEnd(View):
        #   def get(self, request):
        #       return render(request,'dayendversion.html')


class TrunkChDb(View):
    def get(self, request):
        logger.info(request.GET)
        logger.info("--------------TrunkChDb----------------")
        handler_script = settings.VERSION_trunk_chdb_script
        trukchdb_obj = VersionControl('0', script_file=handler_script)
        logger.info(trukchdb_obj)
        logger.info("-------")
        version_list = trukchdb_obj.get_version_list()
        logger.info("------TrunkChDb----------")
        return render(request, 'trunkchdbversion.html', {'version_list': version_list})

    def post(self, request):
        logger.info(request.POST)
        logger.info(request.FILES)
        roll_choice_vers = request.POST.get("roll_choice_vers")
        start_host = request.POST.get("start_host")
        end_host = request.POST.get("end_host")
        myFile = request.FILES.get('v_file_obj', None)
        packge_content = request.POST.get("packge_content")
        trunk_chdb_txt = settings.VERSION_trunk_CHDB_TXT
        logger.info(packge_content)
        logger.info(myFile)
        res_obj = BaseResponse()

        # 拼接python升级回滚的命令
        starttime = datetime.datetime.now()
        if start_host and end_host and start_host <= end_host \
                and start_host.isdigit() and end_host.isdigit():
            endtime = datetime.datetime.now()
            logger.info((endtime - starttime).seconds)
            # 版本回滚
            if roll_choice_vers:
                starttime = datetime.datetime.now()
                trunk_chdb_obj = VersionControl('2', script_file=settings.VERSION_trunk_chdb_script,
                                             action=roll_choice_vers,
                                             start_host=start_host,
                                             end_host=end_host)
                pgadmin_result_str = trunk_chdb_obj.action_func()
                logger.info("--------TrunkChDb 开始回滚 -------------")
                logger.info(pgadmin_result_str)
                res_obj.status = True
                res_obj.data = pgadmin_result_str
                endtime = datetime.datetime.now()
                logger.info((endtime - starttime).seconds)
                # 执行python命令
                logger.info('开始回滚：' + trunk_chdb_result_str)
                result_pgadmin = os.popen(trunk_chdb_result_str).read()
                res_obj.data = result_pgadmin
                # res_obj.data = trunk_chdb_result_str

            elif myFile:
                # 上传文件
                logger.info("--------pgadmin 开始升级-------------")
                if not myFile:
                    res_obj.status = False
                    res_obj.error = "升级包没有上传成功"
                    return HttpResponse(res_obj.__dict__)

                # 打开特定的文件进行二进制的写操作
                destination = open(os.path.join(settings.VERSINO_trunk_CHDB_SOURCE, myFile.name), 'wb+')
                for chunk in myFile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

                trunk_chdb_obj = VersionControl('1',
                                             script_file=settings.VERSION_trunk_chdb_script,
                                             action=myFile.name,
                                             start_host=start_host,
                                             end_host=end_host,
                                             )
                trunk_chdb_result_str = trunk_chdb_obj.action_func()
                logger.info("-----------------")
                logger.info(trunk_chdb_result_str)
                res_obj.status = True
                res_obj.data = trunk_chdb_result_str

                # 打包内容写入
                logger.info("-------------打包内容写入开始-------------")
                package_index = open(trunk_chdb_txt, 'a+')
                package_index.write('\n升级内容：' + packge_content)
                package_index.close()
                logger.info('\n升级包名：' + trunk_chdb_obj.action)
                logger.info('\n打包时间：' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                logger.info("-------------打包内容写入结束-------------")

                # 执行 Python 命令
                logger.info('开始升级:' + trunk_chdb_result_str)
                result_trunk_chdb = os.popen(trunk_chdb_result_str).read()
                res_obj.data = result_trunk_chdb
            else:
                res_obj.status = False
                res_obj.error = "文件名没写"
        else:
            res_obj.status = False
            res_obj.error = "主机参数不完整，请加没插主机范围。示例：【1-2】或者【1-1】"
        logger.info('-------pgadmin执行结束------------')
        logger.info(res_obj.__dict__)

        return HttpResponse(json.dumps(res_obj.__dict__))
