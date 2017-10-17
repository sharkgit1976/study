# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import  View
from oms_web import settings
from dbmanager.models import *
from django.conf import settings
import random,os,sys,json
import time
import ansible.runner

import logging
logger = logging.getLogger('django')

file_name = ""

# Create your views here.

#ansible 执行命令函数
def ansible_shell(config_file, command, pattern, remote_user):
    sout = []
    serr = []
    logger.info("--------------")
    results = ansible.runner.Runner(
        host_list=config_file,
        module_name='shell',
        module_args=command,
        pattern=pattern,
        remote_user=remote_user,
        forks=10
    ).run()

    if results is None:
        logger.info("No hosts found")
        sys.exit(1)
    for (hostname, result) in results['dark'].items():
        logger.info(" %s >>> %s " % (hostname, result))
        serr.append("%s >>> %s \n " % (hostname, result['msg']))
        # sys.exit(-1)
    for (hostname, result) in results['contacted'].items():
        if not 'failed' in result:
            if result['rc'] == 0:
                logger.info("rc = %d  %s >>> %s " % (result['rc'],hostname,result['stdout'].encode('raw_unicode_escape').decode('gbk').encode('utf-8')))                                #print "\033[1;32m %s 命令执行成功 \033[0m" % hostname
                sout.append("%s %s 执行成功\n" % (hostname, command))
            else:
                logger.info("stderr:-->%s \n\n stdout:-->%s\n" % (result['stderr'].encode('raw_unicode_escape').decode('gbk').encode('utf-8'),
                                                                  result['stdout'].encode('raw_unicode_escape').decode('gbk').encode('utf-8')))
                serr.append("%s %s 执行失败\n " % (hostname, command))
                # sys.exit(-1)
        else:
            logger.info (" %s >>> %s " % (hostname, result['msg']))
            serr.append("%s %s 执行失败!-msg:%s\n" % (hostname, command, result['msg']))
            # sys.exit(-1)
    return sout, serr

# ansible script模块相当于scp+shell，将本地脚本在远端minion进行执行
def ansible_script(config_file, command, pattern, remote_user):
    sout = []
    serr = []
    logger.info("--------------")
    results = ansible.runner.Runner(
        host_list=config_file,
        module_name='script',
        module_args=command,
        pattern=pattern,
        remote_user=remote_user,
        forks=10
    ).run()

    if results is None:
        logger.info("No hosts found")
        sys.exit(1)
    for (hostname, result) in results['dark'].items():
        logger.info(" %s >>> %s " % (hostname, result))
        serr.append("%s >>> %s \n " % (hostname, result['msg']))
        # sys.exit(-1)
    for (hostname, result) in results['contacted'].items():
        if not 'failed' in result:
            if result['rc'] == 0:
                sout.append("%s %s 执行成功\n" % (hostname, command))
            else:
                serr.append("%s %s 执行失败\n " % (hostname, command))
        else:
            logger.info (" %s >>> %s " % (hostname, result['msg']))
            serr.append("%s %s 执行失败!-msg:%s\n" % (hostname, command, result['msg']))
    return sout, serr

# ansible 上传文件到远程主机
def ansible_copy(config_file,command,pattern,remote_user):
        sout=[]
        serr=[]
        results = ansible.runner.Runner(
                        host_list=config_file,
                        module_name='copy',
                        module_args=command,
                        pattern=pattern,
                        remote_user=remote_user,
                        forks=10
                        ).run()
        for (hostname, result) in results['dark'].items():
                logger.info("%s >>> %s" % (hostname, result))
                serr.append("%s 拷贝文件失败 %s ！！！\n" % (hostname,result))
                #sys.exit(-1)
        for (hostname, result) in results['contacted'].items():
                if not 'failed' in result:
                        logger.info("%s 拷贝文件成功！！！\n" % (hostname))
                        sout.append("%s 拷贝文件成功！！！\n" % (hostname))
                else:
                        logger.info(" %s 拷贝文件失败 %s!!! " %(hostname,result['msg']))
                        serr.append("%s 拷贝文件失败 %s ！！！\n" % (hostname,result['msg']))
                        #sys.exit(-1)
        return sout,serr

#创建目录
def ansible_file(config_file,command,pattern,remote_user):
        serr=[]
        sout=[]
        results = ansible.runner.Runner(
                        host_list=config_file,
                        module_name='file',
                        module_args=command,
                        pattern=pattern,
                        remote_user=remote_user,
                        forks=10
                        ).run()
        if results is None:
                logger.info(" No hosts found ")
        for (hostname, result) in results['dark'].items():
                logger.info(" %s >>> %s " % (hostname, result))
        for (hostname, result) in results['contacted'].items():
                if 'failed' in result:
                        logger.info("%s >>> %s " % (hostname, result['msg']))
                        serr.append("%s 创建目录[%s]失败！！\n msg->: %s " % (hostname,command.split()[0],result['msg']))
                else:
                        logger.info("在%s 创建目录 %s 成功 " % (hostname, command.split()[0]))
                        sout.append("在%s 创建目录 %s 成功！！！\n" % (hostname, command.split()[0]))

        return sout,serr

#接受选中的IP的数据,生成ansible的配置文件
def ansible_config(request):
    if request.method == 'POST':
        logger.info("----------------")
        logger.info("删除5分钟之前的配置文件")
        logger.info(settings.SERVCIE_DIR)
        rm_comand = "find %s -mmin +5 |xargs rm -f" %  settings.SERVCIE_DIR
	os.system(rm_comand)
        logger.info(rm_comand)
        logger.info(request.POST)
        answer = request.POST.get("answer", "")
        file_group = request.POST.get("file_group", "")
        if answer == "":
            return HttpResponse('{"recode":"fail","msg":"请选择主机！！"}', content_type='application/json')
        logger.info(answer.split(','))

        # 使用随机数 生成文件名
        ran = random.randint(1, 99)
        file_name = file_group +'-'+str(ran)
        file_path = '%s/%s' % (settings.SERVCIE_DIR,file_name)
        file_object = open(file_path, 'w')
        file_object.write('[select]\n')
        try:
            for host in answer.split(','):
                logger.info(host)
                file_object.write(host + '\n')
            file_object.write('\n\n')
            result = "ansible配置文件生成成功"
            logger.info("ansible配置文件生成成功")
        except IOError:
            result = "ansible配置文件生成失败"
            logger.info("ansible配置文件生成失败")
            return HttpResponse('{"recode":"fail","msg":"生成配置文件失败！！"}', content_type='application/json')
        finally:
                file_object.close()

        data={}
        data["recode"] ="success"
        data["file_name"] = file_name
        logger.info(data)

        # return HttpResponse('{"recode":"success"}', content_type='application/json')
        return HttpResponse(json.dumps(data), content_type='application/json')

#get方法的ajax
def tuxedomold(request):
    logger.info(request.GET)
    mold = request.GET.get("mold")
    filename = request.GET.get("filename")
    f_name = filename.split("-")[0]
    data = {}
    if mold == "y":
        print "tuxedo服务全启"
        data["retcode"] = "success"
    elif mold == "s":
        logger.info("查询tuxedo数据库")
        services = TuxedoService.objects.filter(service_group=f_name).values("service_name","service_desc").distinct("service_name")
        logger.info( services)
        for service in services:
            logger.info(service)
        data["retcode"] = "success"
        data["content"] = list(services)
    elif mold == "i":
        logger.info( "查询数据")
	services = TuxedoId.objects.filter(service_group=f_name).values("service_id","service_name","service_desc")
        logger.info(services)
        for service in services:
            logger.info(service)
        data["retcode"] = "success"
        data["content"] = list(services)
    else:
        print "有人恶意篡改,参数错误"
        data["retcode"] = "fail"

    data["mold"] = mold


    return HttpResponse(json.dumps(data), content_type='application/json')

class ServiceStart(View):
    def get(self,request):
        all_hosts = HostList.objects.all()
        group = request.GET.get("group", "")
        area = request.GET.get("area", "")
        print "=================="
        print(settings.CSRF_HEADER_NAME)
        print "=================="
        if group.strip()=='' and group.strip() == '':
            group = 'chmap'

        if group:
            all_hosts = all_hosts.filter(group = group)
            print "xxxxxxxxxxxx"
            for host in all_hosts:
                print host.addip


        if area:
            all_hosts = all_hosts.filter(area=int(area))
            print "-------------xxxx---"
            for host in all_hosts:
                print host.addip

        host_nums = all_hosts.count()
        all_hosts = all_hosts.order_by("addip")
        for host in all_hosts:
            print host.addip

        return render(request,'servicestart.html',{
            "group":group,
            "area" : area,
            "all_hosts":all_hosts,
            "host_nums":host_nums
        })
    def post(self,request):
        command = "平台重启命令"
        start = request.POST.get("start", "")
        stop = request.POST.get("stop", "")
        config_file = request.POST.get("filename", "")
        if config_file == "":
            return HttpResponse('{"recode":"fail","msg":"没有提交选择的主机"}', content_type='application/json')
        logger.info(start)
        logger.info(config_file)

        pattern = "select"
        remote_user = config_file.split('-')[0]
        logger.info(pattern)
        logger.info(remote_user)
        if start == '1':
            command = "source /app/%s/.bash_profile>>/dev/null;sh CH_AppBoot.sh start" % remote_user

        elif stop == '2':
            command = "source /app/%s/.bash_profile>>/dev/null;sh CH_AppBoot.sh stop" % remote_user

        else:
            return HttpResponse('{"recode":"fail","msg":"参数非法,有人恶意访问"}', content_type='application/json')
        config = settings.SERVCIE_DIR + '/' + config_file
        logger.info("====================")
        logger.info(config_file)
        logger.info(config)
        logger.info(command)
        logger.info(pattern)
        logger.info(remote_user)
        logger.info("====================")
        sout, serr = ansible_shell(config, command, pattern, remote_user)
        if serr:
            logger.info("\n".join(serr))
            result = "\n".join(serr)
        else:
            logger.info("\n".join(sout))
            result = "\n".join(sout)

        data = {}
        data["recode"] = "success"
        data["result"] = result

        return HttpResponse(json.dumps(data), content_type='application/json')



class Servcietuxedo(View):
    def get(self,request):
        all_hosts = HostList.objects.all()
        group = request.GET.get("group", "")
        area = request.GET.get("area", "")
        print "=================="
        print(settings.CSRF_HEADER_NAME)
        print "=================="
        if group.strip()=='' and group.strip() == '':
            group = 'chmap'

        if group:
            all_hosts = all_hosts.filter(group = group)
            print "xxxxxxxxxxxx"
            for host in all_hosts:
                print host.addip


        if area:
            all_hosts = all_hosts.filter(area=int(area))
            print "-------------xxxx---"
            for host in all_hosts:
                print host.addip

        host_nums = all_hosts.count()
        all_hosts = all_hosts.order_by("addip")
        for host in all_hosts:
            print host.addip

        return render(request,'servicetuxedo.html',{
            "group":group,
            "area" : area,
            "all_hosts":all_hosts,
            "host_nums":host_nums
        })
    def post(self,request):
        start = request.POST.get("start", "")
        stop = request.POST.get("stop", "")
        mold = request.POST.get("mold", "")
        service_name = request.POST.get("service_name", "")
        service_id = request.POST.get("service_id", "")
        config_file = request.POST.get("filename", "")
        logger.info(mold)
        logger.info(service_name)
        logger.info(service_id)
        if config_file == "":
            return HttpResponse('{"recode":"fail","msg":"没有提交选择的主机"}', content_type='application/json')

        pattern = "select"
        remote_user = config_file.split('-')[0]
        if mold == 'y':
            if start == '1':
                logger.info('tuxedo 程序启动----')
                command = "source /app/%s/.bash_profile>>/dev/null;tmboot -y" % remote_user
            elif stop == '2':
                logger.info("tuxedo 程序停止----")
                command = "source /app/%s/.bash_profile>>/dev/null;tmshutdown -y" % remote_user
            else:
                return HttpResponse('{"recode":"fail","msg":"参数非法,有人恶意访问"}', content_type='application/json')

        if mold == 's':
            if start == '1':
                logger.info('tuxedo s 程序启动----')
                command = "source /app/%s/.bash_profile>>/dev/null;tmboot -s %s" % (remote_user,service_name)
            elif stop == '2':
                logger.info("tuxedo s 程序停止----")
                command = "source /app/%s/.bash_profile>>/dev/null;tmshutdown -s %s" % (remote_user,service_name)
            else:
                return HttpResponse('{"recode":"fail","msg":"参数非法,有人恶意访问"}', content_type='application/json')

        if mold == 'i':
            if start == '1':
                logger.info('tuxedo id 程序启动----')
                command = "source /app/%s/.bash_profile>>/dev/null;tmboot -i %s" % (remote_user, service_id)
            elif stop == '2':
                logger.info("tuxedo id  程序停止----")
                command = "source /app/%s/.bash_profile>>/dev/null;tmshutdown -i %s" % (remote_user, service_id)
            else:
                return HttpResponse('{"recode":"fail","msg":"参数非法,有人恶意访问"}', content_type='application/json')

        config = settings.SERVCIE_DIR + '/' + config_file
        logger.info("====================")
        logger.info(config_file)
        logger.info(config)
        logger.info(command)
        logger.info(pattern)
        logger.info(remote_user)
        logger.info("====================")
        sout, serr = ansible_shell(config, command, pattern, remote_user)
        if serr:
            logger.info("\n".join(serr))
            result = "\n".join(serr)
        else:
            logger.info("\n".join(sout))
            result = "\n".join(sout)

        data={}
        data["recode"] ="success"
        data["result"] = result

        return HttpResponse(json.dumps(data), content_type='application/json')


class Servicesingle(View):
    def get(self,request):
        all_hosts = HostList.objects.all()
        group = request.GET.get("group", "")
        area = request.GET.get("area", "")
        print "=================="
        print(settings.CSRF_HEADER_NAME)
        print "=================="
        if group.strip()=='' and group.strip() == '':
            group = 'chmap'

        if group:
            all_hosts = all_hosts.filter(group = group)
            print "xxxxxxxxxxxx"
            for host in all_hosts:
                print host.addip


        if area:
            all_hosts = all_hosts.filter(area=int(area))
            print "-------------xxxx---"
            for host in all_hosts:
                print host.addip

        host_nums = all_hosts.count()
        all_hosts = all_hosts.order_by("addip")
        for host in all_hosts:
            print host.addip

        #singles = TuxedoSingle.objects.all()
        singles = TuxedoSingle.objects.filter(single_group=group)
        for  single in singles:
            print single.single_command


        return render(request,'servicesingle.html',{
            "group":group,
            "area" : area,
            "all_hosts":all_hosts,
            "singles":singles,
            "host_nums":host_nums
        })

    def post(self,request):
        start = request.POST.get("start", "")
        stop = request.POST.get("stop", "")
        config_file = request.POST.get("filename", "")
        single_command = request.POST.get("single_command", "")
        logger.info(single_command)
        if config_file == "":
            return HttpResponse('{"recode":"fail","msg":"没有提交选择的主机"}', content_type='application/json')
        print start,config_file
        # ansible 使用的参数
        pattern = "select"
        remote_user = config_file.split('-')[0]

        shell_name = single_command.split('-')[0]
        shell_para = single_command.split('-')[1]
        if start == '1':
            rm_shell = "find %s -mmin +5 |xargs rm -f" % settings.SHELL_DIR
            os.system(rm_shell)
            # --- 生成执行脚本 -----
            shell_file = '%s/%s.sh' % (settings.SHELL_DIR, single_command)
            file_object = open(shell_file, 'w')
            #pub = 'source /app/%s/.bash_profile \n' % remote_user
            #file_object.write(pub)
            try:
                for i in range(settings.PROCESS_NUM):
                    file_object.write(shell_name +' '+ shell_para + '  &\n')
                tmp = 'ps -ef|grep %s|grep %s|grep -v grep' % (shell_name,shell_para)
                file_object.write(tmp)
                file_object.write('\n')
                logger.info("shell执行脚本生成成功")
            except IOError:
                logger.info("shell执行脚本生成失败")
                return HttpResponse('{"recode":"fail","msg":"shell执行脚本生成失败！！"}', content_type='application/json')
            finally:
                file_object.close()
            # 创建目录

            # 使用 ansible 执行 shell 脚本
            logger.info("开始执行脚本")
            logger.info("====================")
            logger.info(config_file)
            logger.info(shell_file)
            logger.info(pattern)
            logger.info(remote_user)
            logger.info("====================")
            #建立远程目录
            config = settings.SERVCIE_DIR + '/' + config_file
            command = 'path=/app/%s/shell state=directory mode=0755' % (remote_user)
            logger.info(command)
            ansible_file(config, command, pattern, remote_user)

            # 拷贝脚本到远程主机
            command = 'src=%s dest=/app/%s/shell backup=yes' % (shell_file, remote_user)
            logger.info(command)
            sout, serr = ansible_copy(config, command, pattern, remote_user)
            print sout, serr
            if serr:
                logger.info("\n".join(serr))
                result = "\n".join(serr)
            else:
                logger.info("\n".join(sout))
                result = "\n".join(sout)

            # 远程执行脚本
            command = "source /app/%s/.bash_profile;sh /app/%s/shell/%s.sh" % (remote_user,remote_user,single_command)
            logger.info(command)
            sout, serr = ansible_shell(config, command, pattern, remote_user)
            if serr:
                logger.info("\n".join(serr))
                result = "\n".join(serr)
            else:
                logger.info("\n".join(sout))
                result = "\n".join(sout)

            command = "find /app/%s/shell -mmin +10 |xargs  rm -f  " % remote_user
            logger.info(command)
            #ansible_shell(config, command, pattern, remote_user)


        elif stop  == '2':
            config = settings.SERVCIE_DIR + '/' + config_file
            command = "ps -ef|grep %s|grep %s|grep -v /bin/sh|awk \'{print $2}\'|xargs kill -9" % (shell_name,shell_para)
            sout, serr = ansible_shell(config, command, pattern, remote_user)
            if serr:
                logger.info("\n".join(serr))
                result = "\n".join(serr)
            else:
                logger.info("\n".join(sout))
                result = "\n".join(sout)
        else:
            return HttpResponse('{"recode":"fail","msg":"参数非法,有人恶意访问"}', content_type='application/json')

        data={}
        data["recode"] ="success"
        data["result"] = result

        return HttpResponse(json.dumps(data), content_type='application/json')
