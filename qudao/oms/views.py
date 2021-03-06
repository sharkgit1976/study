# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import  View
from oms_web.mysql import db_operate
from oms_web.postgre import pg2_operate
from oms_web import settings
import  os,json,psycopg2,MySQLdb
from dbmanager.models import HostList,SelectHost
from oms.models import *
import ansible.runner

# 分页 --应用的库
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


import datetime


import logging
logger = logging.getLogger('django') 
# Create your views here.
mret=""
cmdrun_txt=""
HostManage_value=""
dbmanage_txt=""
col_name=[]
pg2manage_txt=""
as_error = {}
as_correct = {}



def index(request):
    now = datetime.datetime.now()
    my_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print my_time
    os.system('ls ')
    return render(request,'index.html',{'datetime':my_time})

def remote_exec(request):
    if request.method == 'POST':
	global mret
        host = request.POST.get('host', '')
        command = request.POST.get('command', '')
        host='127.0:0.1,22,ansible,123,'
        logger.info('xxxxxxxxxxxxxxxxxxxxxxxxxx') 
        tmphost = host.split(',')
        hostip   = tmphost[0]
        port     = tmphost[1]
        username = tmphost[2]
        passwd   = tmphost[3]
        logger.info(hostip + port + username + passwd+ command) 
        resp = os.popen(command).readlines()
        logger.info('xxxxxxxxxxxxxxxxxxxxxxxxxx') 
        logger.info(resp) 
        mret = "输入内容如下:\n" +"*************************\n"+ "".join(resp)
        logger.info(mret)
    return render(request,'ssh.html',{ 'mret':mret })

# def HostManage(request):
#     if request.method == 'POST':
#         global HostManage_value
#         hostlist   = request.POST.get('hostlist','')
#         logger.info(hostlist)
#         command = "sudo echo \"" +hostlist+ " \">> /etc/ansible/hosts "
#         logger.info(command)
#         m = os.system(command)
#         if m == 0:
#             logger.info(command+"执行成功！！！！")
#         else:
#             return render(request,'hostmanage.html',{'HostManage_txt':"主机配置失败！！"})
#         HostManage_txt = os.popen('cat /etc/ansible/hosts').readlines()
#         HostManage_value=''.join(HostManage_txt)
#         logger.info(HostManage_value)
#     return render(request,'hostmanage.html',{'HostManage_txt':HostManage_value})





class cmdrun(View):
    def get(self, request):
        as_corrects = ansible_result.objects.order_by("-status", "hostip")  # 获取ansible输出信息
        logger.info('----------------------------------')
        logger.info(as_corrects)
        for as_correct in as_corrects:
            logger.info(as_correct.hostip)
        logger.info('----------------------------------')
        # # ansible换回信息  分页 顺序
        try:
            page2 = request.GET.get('page', 1)
        except PageNotAnInteger:
            page2 = 1

        p = Paginator(as_corrects, settings.PAGING, request=request)

        corrects = p.page(page2)
        for correct in corrects.object_list:
            logger.info(correct.id)
        return render(request, 'cmdrun.html',locals())

    def post(self, request):

        # 组
        group = request.POST.get('group', '')
        # 模块
        my_model = request.POST.get('ansible', '')
        # 命令参数
        mrcommand = request.POST.get('mrcommand', '')
        logger.info("获取的表单数据:group:[" + group + "],my_model:[" + my_model + "],mrcommand:[" + mrcommand + "]")

        logger.info('xxxxxxxxxxxxxxxxxxxxx'+request.user.username)
        if mrcommand:
            if request.user.username not in settings.USER_PERMISSION:
                logger.info(request.user.username+"不是超级用户")
                if mrcommand.strip().split()[0] in settings.COMMAND_PERMISSION:
                    logger.info("哎！你的老大看见你这样操作会不开心的~~")
                    return render(request, "cmdrun.html", {'message_txt': '哎！你的老大看见你这样操作会不开心的~~'})
        if my_model != "ping":
            if not my_model.strip():
                logger.info("模块不能为空")
                return render(request, "cmdrun.html", {'message_txt': "亲!!模块没有选择"})
            if my_model != "copy" and my_model != "fetch" and not mrcommand.strip():
                logger.info("命令行不能为空")
                return render(request, "cmdrun.html", {'message_txt': "亲，命令没输，这么粗心怎么能上王者"})

        if my_model == 'copy' or my_model == 'fetch':
            localCommand = request.POST.get('localCommand', '')
            remoteCommand = request.POST.get('remoteCommand', '')
            logger.info("xxxxxxxxxxxxxxxxx" + localCommand + remoteCommand)
            if not localCommand.strip():
                logger.info("本地文件不能为空")
                return render(request, "cmdrun.html", {'message_txt': "本地文件不能为空"})
            if not remoteCommand.strip():
                logger.info("远程目标文件不能为空")
                return render(request, "cmdrun.html", {'message_txt': "远程目标文件不能为空"})
            if my_model == "copy":
                temp = "src=" + localCommand + " dest=" + remoteCommand + " backup=yes"
            else:
                temp = "src=" + localCommand + " dest=" + remoteCommand
            logger.info(temp)

        else:
            temp = mrcommand

        results = []
        if group == "select":
            logger.info("----连接数据库，生成文件---")
            logger.info(settings.ANSIBLE_HOSTS_FILE)
            cmd = "rm -f " + settings.ANSIBLE_HOSTS_FILE
            logger.info(cmd)
            os.system(cmd)
            file_object = open(settings.ANSIBLE_HOSTS_FILE, 'w')
            try:
                selectgp = SelectHost.objects.values('selectgroup').distinct().order_by('selectgroup')
                for gp in selectgp:
                    logger.info(gp['selectgroup'])
                    file_object.write('[' + gp['selectgroup'] + ']\n')
                    hosts = SelectHost.objects.filter(selectgroup=gp['selectgroup'])  # 获取主机组的信息
                    for host in hosts:
                        logger.info(host.selectip)
                        file_object.write(host.selectip + '\n')
                    file_object.write('\n\n')
            finally:
                file_object.close()

            # 清空数据库
            # SelectHost.objects.all().delete()
            # 指定的hosts文件，选择主机


            global as_currect
            global as_error

            cmdrun_tp = []
            logger.info("==========================")
            logger.info(selectgp)
            for gp in selectgp:
                logger.info(gp['selectgroup'])
                # 模块名 命令行参数 主机组 远程用户名
                logger.info("==========" + settings.ANSIBLE_HOSTS_FILE)
                results = ansible.runner.Runner(
                    host_list=settings.ANSIBLE_HOSTS_FILE,
                    module_name=my_model,
                    module_args=temp,
                    pattern=gp['selectgroup'],
                    remote_user=gp['selectgroup'],
                    forks=10
                ).run()

                # 返回结果处理
                # 删除ansible信息表中的内容
                logger.info("-------删除ansible信息表中的内容---------")
                ansible_result.objects.all().delete()
                logger.info("-----------选择主机输出-------------------")
                if results is None:
                    list.append("No hosts found")
                    return render(request, "cmdrun.html")
                if my_model == 'ping':
                    for (hostname, result) in results['contacted'].items():
                        if not 'failed' in result:
                            correct = ansible_result(hostip=hostname, asmsg=result['ping'], status='0')
                            correct.save()

                            logger.info(u"\n主机：%s \n输出的内容:---->\n%s\n" % (hostname, result['ping']))
                elif my_model == 'copy':
                    for (hostname, result) in results['contacted'].items():
                        if not 'failed' in result:
                            correct_txt = u"%s 拷贝文件成功！！！\n" % (hostname)
                            correct = ansible_result(hostip=hostname, asmsg=correct_txt, status='0')
                            correct.save()
                            # i = i + 1
                            logger.info(u"\n主机：%s 拷贝文件成功！！！\n" % (hostname))
                elif my_model == 'fetch':
                    for (hostname, result) in results['contacted'].items():
                        if not 'failed' in result:
                            correct_txt = u"%s 获取文件成功！！！\n" % (hostname)
                            correct = ansible_result(hostip=hostname, asmsg=correct_txt, status='0')
                            correct.save()
                            logger.info(u"\n主机：%s 获取文件成功！！！\n" % (hostname))
                else:
                    for (hostname, result) in results['contacted'].items():
                        if not 'failed' in result:
                            if result['rc'] == 0:
                                logger.info('---------------------currect_msg----------------------')
                                logger.info(
                                result['stdout'].encode('raw_unicode_escape').decode('gb18030').encode('utf-8'))
                                correct = ansible_result(hostip=hostname,
                                                         asmsg=result['stdout'].encode('raw_unicode_escape').decode(
                                                             'gbk').encode('utf-8'), status='0')
                                correct.save()
                            else:
                                logger.info('-----------------err_msg-------------------------')
                                err_msg = ("stderr:-->%s \n\n stdout:-->%s\n") % (
                                result['stderr'].encode('raw_unicode_escape').decode('gbk').encode('utf-8'),
                                result['stdout'].encode('raw_unicode_escape').decode('gbk').encode('utf-8'))
                                correct = ansible_result(hostip=hostname, asmsg=err_msg, status='1')
                                correct.save()
                for (hostname, result) in results['contacted'].items():
                    if 'failed' in result:
                        correct = ansible_result(hostip=hostname, asmsg=result['msg'], status='1')
                        correct.save()
                        logger.info(u"\n主机：%s \n 错误信息:------>\n%s\n" % (hostname, result['msg']))
                for (hostname, result) in results['dark'].items():
                    correct = ansible_result(hostip=hostname, asmsg=result['msg'], status='1')
                    correct.save()
                    logger.info(u"\n失败主机:%s\n 输出的内容:--->\n%s\n" % (hostname, result))
                logger.info("-----------------")

        else:
            logger.info(settings.ANSIBLE_ALL_HOST + 'xxxxxxxxxx')
            results = ansible.runner.Runner(
                host_list=settings.ANSIBLE_ALL_HOST,
                module_name=my_model,
                module_args=temp,
                pattern=group,
                remote_user=group,
                forks=10
            ).run()

            # 返回结果处理
            # 删除ansible信息表中的内容
            logger.info("-------删除ansible信息表中的内容---------")
            ansible_result.objects.all().delete()
            logger.info("-------返回结果处理---------")
            if results is None:
                list.append("No hosts found")
                return render(request, "cmdrun.html")
            if my_model == 'ping':
                for (hostname, result) in results['contacted'].items():
                    if not 'failed' in result:
                        correct = ansible_result(hostip=hostname, asmsg=result['ping'],status='0')
                        correct.save()

                        logger.info(u"\n主机：%s \n输出的内容:---->\n%s\n" % (hostname, result['ping']))
            elif my_model == 'copy':
                for (hostname, result) in results['contacted'].items():
                    if not 'failed' in result:
                        correct_txt = u"%s 拷贝文件成功！！！\n" % (hostname)
                        correct = ansible_result(hostip=hostname, asmsg=correct_txt,status='0')
                        correct.save()
                        # i = i + 1
                        logger.info(u"\n主机：%s 拷贝文件成功！！！\n" % (hostname))
            elif my_model == 'fetch':
                for (hostname, result) in results['contacted'].items():
                    if not 'failed' in result:
                        correct_txt = u"%s 获取文件成功！！！\n" % (hostname)
                        correct = ansible_result(hostip=hostname, asmsg=correct_txt,status='0')
                        correct.save()
                        logger.info(u"\n主机：%s 获取文件成功！！！\n" % (hostname))
            else:
                for (hostname, result) in results['contacted'].items():
                    if not 'failed' in result:
                        if result['rc'] == 0:
                            logger.info('---------------------currect_msg----------------------')
                            logger.info(result['stdout'].encode('raw_unicode_escape').decode('gb18030').encode('utf-8'))
                            correct = ansible_result(hostip=hostname, asmsg=result['stdout'].encode('raw_unicode_escape').decode('gbk').encode('utf-8'),status='0')
                            correct.save()
                        else:
                            logger.info('-----------------err_msg-------------------------')
                            err_msg = ("stderr:-->%s \n\n stdout:-->%s\n") % (result['stderr'].encode('raw_unicode_escape').decode('gbk').encode('utf-8'),result['stdout'].encode('raw_unicode_escape').decode('gbk').encode('utf-8'))
                            correct = ansible_result(hostip=hostname, asmsg=err_msg, status='1')
                            correct.save()
                        logger.info(u"\n主机：%s \n输出的内容:---->\n%s\n" % (hostname, result['stdout']))
            for (hostname, result) in results['contacted'].items():
                if 'failed' in result:
                    correct = ansible_result(hostip=hostname, asmsg=result['msg'],status='1')
                    correct.save()
                    logger.info(u"\n主机：%s \n 错误信息:------>\n%s\n" % (hostname, result['msg']))
            for (hostname, result) in results['dark'].items():
                correct = ansible_result(hostip=hostname, asmsg=result['msg'],status='1')
                correct.save()
                logger.info(u"\n失败主机:%s\n 输出的内容:--->\n%s\n" % (hostname, result))
            logger.info("-----------------")

        as_corrects = ansible_result.objects.order_by("-status", "hostip")  # 获取ansible输出信息
        logger.info('----------------------------------')
        logger.info(as_corrects)
        for as_correct in as_corrects:
            logger.info(as_correct.hostip)
        logger.info('----------------------------------')
        # # ansible换回信息  分页 顺序
        try:
            page2 = request.GET.get('page', 1)
        except PageNotAnInteger:
            page2 = 1

        p = Paginator(as_corrects, settings.PAGING, request=request)

        corrects = p.page(page2)
        for correct in corrects.object_list:
            logger.info(correct.id)
        # return render(request,"cmdrun.html")
        logger.info(corrects)
        return render(request, "cmdrun.html",{"corrects":corrects})

def dayend(request):
    return render(request,'dayend.html')


def dbmanage(request):
    if request.method == 'POST':
        global dbmanage_txt
        sqlOrder = request.POST.get('sqlOrder', '').strip()
        if not sqlOrder:
            logger.info("SQL 为空")
            return render(request, 'dbmanage.html')

        db = db_operate()
        logger.info(settings.REMOTE_MYSQL)
        conn = db.mysql_open(settings.REMOTE_MYSQL)
        logger.info(conn)
        if conn == -1:
            logger.info(u"数据连接错误！！！");
            return render(request, 'dbmanage.html', {'dbmanage_txt': "数据库连接错误！！"})
        logger.info(sqlOrder)
        # result=db.mysql_command(conn,sqlOrder)

        # 找出字段名
        global col_name
        if sqlOrder.strip().split()[0] == "select":
            try:
               cur = conn.cursor(MySQLdb.cursors.DictCursor)
               m = cur.execute(sqlOrder)
               retname = cur.fetchall()
               logger.info(retname)
               logger.info(retname[0])
               for key in retname[0]:
                   logger.info("xxxxxxxxx" + key)
                   col_name.append(key)
               logger.info(retname[0])
               logger.info(col_name)
               # 操作数据
               cursor = conn.cursor()
               n = cursor.execute(sqlOrder)
               logger.info(n)
               results = cursor.fetchall()
               logger.info(results)

               dbmanage_txt = results
               for item in results:
                   logger.info(item)

            except MySQLdb.Error, e:
               logger.info("ssssssssssssssssssss")
               logger.info(e)
               db.mysql_close(conn)
               return render(request, 'dbmanage.html', {'dbmanage_txt': "SQL命令查询失败！！","msg":e.args[1]})


        if sqlOrder.strip().split()[0] == "update":
            # 操作数据
            try:
               cursor = conn.cursor()
               cursor.execute(sqlOrder)
               conn.commit()
               return render(request, 'dbmanage.html', {'dbvalue_txt': "SQL语句更新成功！！！！"})
            except MySQLdb.Error, e:
                logger.info(e)
                conn.rollback()
                db.mysql_close(conn)
                return render(request, 'dbmanage.html', {'dbmanage_txt': "SQL命令执行失败！！","msg":e.args[1]})

        if sqlOrder.strip().split()[0] == "delete":
            # 操作数据
            try:
               cursor = conn.cursor()
               cursor.execute(sqlOrder)
               conn.commit()
               return render(request, 'dbmanage.html', {'dbvalue_txt': "SQL语句删除成功！！！！"})
            except MySQLdb.Error, e:
                logger.info(e)
                conn.rollback()
                db.mysql_close(conn)
                return render(request, 'dbmanage.html', {'dbmanage_txt': "SQL命令执行失败！！","msg":e.args[1]})

        if sqlOrder.strip().split()[0] == "insert":
            # 操作数据
            try:
               cursor = conn.cursor()
               cursor.execute(sqlOrder)
               conn.commit()
               return render(request, 'dbmanage.html', {'dbvalue_txt': "SQL语句插入成功！！！！"})
            except MySQLdb.Error, e:
                logger.info(e)
                conn.rollback()
                db.mysql_close(conn)
                return render(request, 'dbmanage.html', {'dbmanage_txt': "SQL命令执行失败！！","msg":e.args[1]})


        cl = db.mysql_close(conn)
        if cl == -1:
           logger.info(u"关闭数据库失败！！！");
           return render(request, 'dbmanage.html', {'dbmanage_txt': "关闭数据库失败！！"})

        # return render(request,'dbmanage.html',{'n':n,'m':m,'db_keys':keys,'db_values':values})
    return render(request, 'dbmanage.html', {'dbvalue_txt': dbmanage_txt, 'col_names': col_name})

def pg2manage(request):
    if request.method == 'POST':
        global pg2manage_txt
        sqlOrder = request.POST.get('sqlOrder', '').strip()
        if not sqlOrder:
            logger.info("SQL 为空")
            return render(request, 'pg2manage.html')

        pg2 = pg2_operate()
        logger.info(settings.REMOTE_POSTGRES)
        conn = pg2.pg2_open(settings.REMOTE_POSTGRES)
        logger.info(conn)
        if conn == -1:
            logger.info(u"数据连接错误！！！");
            return render(request, 'pg2manage.html', {'pg2manage_txt': "数据库连接错误！！"})
        logger.info(sqlOrder)

        # 找出字段名
        global col_name
        if sqlOrder.strip().split()[0] == "select":
            try:

                # 操作数据
                cursor = conn.cursor()
                n = cursor.execute(sqlOrder)
                results = cursor.fetchall()
                logger.info(results)
                col_name = "col_name"
                pg2manage_txt = results
                for item in results:
                    logger.info(item)

            except psycopg2.Error, e:
                logger.info(str(e))
                pg2.pg2_close(conn)
                return render(request, 'pg2manage.html', {'pg2manage_txt': "SQL命令查询失败！！",'msg':str(e)})

        if sqlOrder.strip().split()[0] == "update":
            # 操作数据
            try:
                cursor = conn.cursor()
                cursor.execute(sqlOrder)
                conn.commit()
                return render(request, 'pg2manage.html', {'dbvalue_txt': "SQL语句更新成功！！！！"})
            except psycopg2.Error, e:
                logger.info(str(e))
                conn.rollback()
                pg2.pg2_close(conn)
                return render(request, 'pg2manage.html', {'pg2manage_txt': "SQL命令执行失败！！","msg":str(e)})

        if sqlOrder.strip().split()[0] == "delete":
            # 操作数据
            try:
                cursor = conn.cursor()
                cursor.execute(sqlOrder)
                conn.commit()
                return render(request, 'pg2manage.html', {'dbvalue_txt': "SQL语句删除成功！！！！"})
            except psycopg2.Error, e:
                logger.info(str(e))
                conn.rollback()
                pg2.pg2_close(conn)
                return render(request, 'pg2manage.html', {'pg2manage_txt': "SQL命令执行失败！！","msg":str(e)})

        if sqlOrder.strip().split()[0] == "insert":
            # 操作数据
            try:
                cursor = conn.cursor()
                n=cursor.execute(sqlOrder)
                logger.info(n)
                conn.commit()
                return render(request, 'pg2manage.html', {'dbvalue_txt': "SQL语句插入成功！！！！"})
            except psycopg2.Error, e:
                logger.info(str(e))
                conn.rollback()
                pg2.pg2_close(conn)
                return render(request, 'pg2manage.html', {'pg2manage_txt': "SQL命令执行失败！！","msg":str(e)})

        cl = pg2.pg2_close(conn)
        if cl == -1:
            logger.info(u"关闭数据库失败！！！")
            return render(request, 'pg2manage.html', {'pg2manage_txt': "关闭数据库失败！！"})

    return render(request, 'pg2manage.html', {'dbvalue_txt': pg2manage_txt, 'col_names': col_name})

class Autodeploy(View):
    def get(self,request):
        xtbs = request.GET.get('xtbs', "")
        print xtbs
        if xtbs.strip():
            if xtbs == 'ps':
                print xtbs
        yybs = request.GET.get('yybs', "")
        print yybs
        if yybs.strip():
            if yybs == 'lj':
                print yybs
                resp = os.popen("ls").readlines()
                logger.info(resp)
                mret = "输入内容如下:\n" + "*************************\n" + "".join(resp)
                print mret
        return render(request,"autodeploy.html")





