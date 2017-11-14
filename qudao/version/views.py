# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
import logging
import os
<<<<<<< HEAD
logger = logging.getLogger('django')
logger.info('ytest')
from oms_web import settings
import datetime

# Create your views here.


class BaseResponse:
=======
import datetime
from oms_web import settings
import json

logger = logging.getLogger('django')
logger.info('ytest')


from django.http import HttpResponse, HttpResponseNotFound

from django.http import Http404
from django.shortcuts import render_to_response

def detail(requests):
    p = '233'
    try:
        obj = getattr(settings, 'ddd')
    except Exception:
        raise Http404("Poll does not exist")
    return render_to_response('404.html', {'poll': p})

def my_view(request):
    # ...
    foo = True
    if foo:
        return HttpResponseNotFound('<h1>Page not yan found</h1>')
    else:
        return HttpResponse('<h1>Page was found</h1>')

class BaseResponse:
    '''
    返回给前端的基础信息格式
    '''
>>>>>>> bac
    def __init__(self):
        self.status = False
        self.data = None
        self.error = None


class VersionControl(object):
<<<<<<< HEAD
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
=======
    '''
    组合成执行命令的字符串
    '''
    def __init__(self,action, script_file='',
                 scritpt_dir=settings.VERSION_SCRIPT_DIR,
                 action_arg='',
                 start_host='',
                 end_host='',
                 ):
        self.action           = action
        self.action_arg       = ' {}'.format(action_arg)
        self.start_host       = ' {}'.format(start_host)
        self.script_file      = script_file
        self.script_dir       = scritpt_dir
        self.end_host         = end_host
        self.script_full_path = os.path.join(self.script_dir, self.script_file)
        self.cmd_run_str      = 'python {} {}'.format(self.script_full_path, self.action)
        logger.info(self.cmd_run_str)
    def get_version_list(self):
        '''
        获取版本列表
        :return: 包含历史版本号的列表
        '''
        logger.info('yan>>{}'.format(self.action))
        logger.info('yan>>{}'.format(self.cmd_run_str))
        self.result_str = os.popen(self.cmd_run_str).read()

        logger.info(self.result_str.split(':'))

        self.version_list = self.result_str.split(':')[1].strip().split('\n')
        # self.version_list = ['20170824', '20170825', '20170826']
>>>>>>> bac
        self.version_list.reverse()
        return self.version_list

    def action_func(self):
        """
<<<<<<< HEAD
          测试是使用  host_range = 8-8
        :return:
        """
        self.cmd_run = self.cmd_run +  self.action + self.start_host + '-' + self.end_host
=======
        组合升级或者回滚的命令字符串
          测试是使用  host_range = 8-8
        :return:
        """
<<<<<<< HEAD
        self.cmd_run = self.cmd_run +  self.action_arg + self.start_host + '-' + self.end_host
>>>>>>> bac
        # self.result_str = os.popen(self.cmd_run).read()
        self.result_str = self.cmd_run
=======
        self.cmd_run_str = self.cmd_run_str +  self.action_arg + self.start_host + '-' + self.end_host
        # self.result_str = os.popen(self.cmd_run_str).read()
        self.result_str = self.cmd_run_str
>>>>>>> shark
        return self.result_str

<<<<<<< HEAD
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
=======
def value_handler(request, arg):
    '''
    根据从 url 处得到的参数不同，来定义出不同的主机组对应的变量值。
    :param request: Http 请求本身
    :param arg: 主机组名
    :return: 需要执行命令的 字符串
    '''
    group_name = arg.upper()
    print('GET - group_name>>>:', group_name)

    if group_name == 'TELLERCHDB':
        handler_script = settings.VERSION_TELLER_CHDB_SCRIPT
        src_dir        = settings.VERSION_TELLER_CHDB_SOURCE
        v_cont_txt     = settings.VERSION_TELLER_CHDB_TXT
        host_range     = settings.CHDB_HOST

    elif group_name == 'CHMAP':
        handler_script = settings.VERSION_CHMAP_SCRIPT
        src_dir        = settings.VERSION_CHMAP_SOURCE
        v_cont_txt     = settings.VERSION_CHMAP_TXT
        host_range = settings.CHMAP_HOST
    elif group_name == 'CHAGENT':
        handler_script = settings.VERSION_CHAGENT_SCRIPT
        src_dir        = settings.VERSION_CHAGENT_SOURCE
        v_cont_txt     = settings.VERSION_CHAGENT_TXT
        host_range = settings.CHAGENT_HOST
    elif group_name == 'TRUNKCHDB':
        handler_script = settings.VERSION_TRUK_CHDB_SCRIPT
        src_dir = settings.VERSION_TRUNK_CHDB_SOURCE
        v_cont_txt = settings.VERSION_TRUNK_CHDB_TXT
        host_range = settings.PGADMIN_HOST
    elif group_name == 'CHCOM':
        handler_script = settings.VERSION_CHCOM_SCRIPT
        src_dir = settings.VERSION_CHCOM_SOURCE
        v_cont_txt = settings.VERSION_CHCOM_TXT
        host_range = settings.CHCOM_HOST
    else:
        handler_script = ''
        src_dir        = ''
        v_cont_txt     = ''
        host_range     = ''

    return host_range, v_cont_txt, src_dir, handler_script, group_name


def host_range_clean(start_host, end_host):
    if start_host and end_host:
        try:
            start_host_n = int(start_host)
            end_host_n = int(end_host)
        except ValueError:
            return False, ''
        else:
            if start_host_n <= end_host_n:
                return start_host_n, end_host_n
            else:
                return False, ''
    else:
        return False, ''


class ChDb(View):
    def get(self, request, arg):
        logger.info(request.GET)
        logger.info("------------------------------")
        host_range, v_cont_txt, src_dir, handler_script, group_name = value_handler(request, arg)

        if handler_script:
            chdb_obj     = VersionControl('0', script_file=handler_script)
            version_list = chdb_obj.get_version_list()

            logger.info("------{}----------".format(group_name))
<<<<<<< HEAD
            return render(request, '{}sversion.html'.format(group_name), locals())
>>>>>>> bac
=======
            return render(request, '{}version.html'.format(group_name.lower()), locals())
>>>>>>> shark
        else:
            # return HttpResponseNotFound('<h1>Page not yan found</h1>')
            p = 'yan error'
            return render_to_response('404.html', {'poll': p })
    def post(self, request, arg):
<<<<<<< HEAD
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
=======
        host_range, v_cont_txt, src_dir, handler_script, group_name = value_handler(request, arg)
        logger.info('POST - goup_name>>>:', group_name)
        logger.info('request post>:{}'.format(request.POST))
        logger.info('request file>:{}'.format(request.FILES))

        roll_choice_vers = request.POST.get("roll_choice_vers", '')
        start_host       = request.POST.get("start_host", '')
        end_host         = request.POST.get("end_host", '')
        res_obj          = BaseResponse()

        start_host_n, end_host_n = host_range_clean(start_host, end_host)

        if (start_host_n in host_range)  and (end_host_n in host_range):
            if roll_choice_vers:
                '''
                版本回滚
                '''
                chdb_obj = VersionControl('2',
                                      script_file=handler_script,
                                      action_arg=roll_choice_vers,
                                      start_host=start_host,
                                      end_host=end_host,
                                      )

                logger.info('{}  开始回滚'.format(group_name))
                chdb_result_str = chdb_obj.action_func()
                logger.info('执行命令：{}'.format(chdb_result_str))
                try:
                    response = os.popen(chdb_result_str).read()
                except Exception as e:
                    res_obj.error = e
                else:
                    # 返回回滚命令执行过程
                    res_obj.status = True
                    res_obj.data   = response

            else:
                '''
                版本升级
                '''
                file_obj = request.FILES.get('v_file_obj', '')
                packge_content = request.POST.get("packge_content")

                logger.info(packge_content)
                logger.info(file_obj)

                if not file_obj:
                    res_obj.error = "上传文件为空"
                elif not packge_content:
                    res_obj.error = "请输入编译后，需要升级打包的内容"
                else:
                    inp_v_name = file_obj.name
                    logger.info("File Name>>:%s" % inp_v_name)

                    # 开始接收文件，并写入到服务器的指定目录下
                    # 组合文件的完整路径
                    # 第一个参数是路径，第二个参数是文件名
                    file_full_path = os.path.join(src_dir, file_obj.name)
                    logger.info('file_path>>{}'.format(file_full_path))
                    # 保存上传的文件
                    with open(file_full_path, 'wb') as new_file_obj:
                        [new_file_obj.write(chunk) for chunk in file_obj.chunks()]
                    if os.path.isfile(file_full_path):
                        logger.info('{}保存成功'.format(new_file_obj))

                    logger.info('\n打包开始时间：' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                    chdb_obj = VersionControl('1',
                                              script_file=handler_script,
                                              action_arg=inp_v_name,
                                              start_host=start_host,
                                              end_host=end_host,
                                              )

                    # 写入需要打包升级的目录名或文件名
                    logger.info("-------------开始写入打包的后需要升级内容-------------")
                    logger.info('\n升级包名：' + chdb_obj.action_arg)
                    logger.info('\n打包开始时间：{}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                    with open(v_cont_txt, 'a+') as package_index:
                        package_index.write('需要打包升级的目录名或文件名：{}\n'.format(packge_content))

                    logger.info('\n打包结束时间：{}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    logger.info("-------------打包内容写入结束-------------")


                    chdb_result_str = chdb_obj.action_func()
                    logger.info('准备开始{}升级{}'.format(group_name,chdb_result_str))
                    logger.info('准备执行升级命令：{}'.format(chdb_result_str))
                    try:
                        response = os.popen(chdb_result_str).read()
                    except Exception as e:
                        res_obj.error = e
                    else:
                        res_obj.status = True
                        res_obj.data   = response

        else:
            res_obj.status = False
            res_obj.error = u"主机参数不正确，请检查主机范围;有效的主机范围是：{}".format(host_range)
        data = json.dumps(res_obj.__dict__)
        logger.info(data)
>>>>>>> bac
        return HttpResponse(data)

def page_not_found(request):

    return render_to_response('404.html')
