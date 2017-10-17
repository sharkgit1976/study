# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import  View
from oms_web import settings
from dbmanager.models import *
from django.conf import settings
from monitor.redis_pub import RedisMonitor,new_request
import json,time
import random,datetime

import logging
logger = logging.getLogger('django')




# Create your views here.
class MonitorRedis(View):
    def get(self,request):
        redis_infos = RedisInfo.objects.all().order_by("redis_ip")
        result = {}
        for redis_info in redis_infos:
            logger.info(redis_info.redis_ip)
            m = new_request(redis_info.redis_ip, redis_info.redis_port, '')
            #logger.info(json.dumps(m,indent=4))
            ping = RedisMonitor().ping(redis_info.redis_ip, redis_info.redis_port, '')
            logger.info(ping)
            list = {}
            # ping : 1 成功 0 失败
            list["ping"] = ping["success"]
            if ping["success"] == 1:
                list["used_memory_human"] = m["data"]["used_memory_human"]
                list["port"] = m["data"]["tcp_port"]
                list["ip"] = redis_info.redis_ip
                list["used_memory_peak_human"] = m["data"]["used_memory_peak_human"]
                if m["data"].has_key("db0"):
                    list["keys"] = m["data"]["db0"]["keys"]

                else:
                    list["keys"] = 0
                list["role"] = m["data"]["role"]
                list["instantaneous_ops_per_sec"] = m["data"]["instantaneous_ops_per_sec"]
            logger.info(list)
            name=redis_info.redis_ip+':'+redis_info.redis_port
            result[name] = list
        logger.info(result)
        return render(request, 'monitorredis.html',{'result':result})

class MonitorRedisInfo(View):
    def get(self,request):
        logger.info(request.GET)
        redis_ip = request.GET.get('redis_ip', '')
        redis_port = request.GET.get('redis_port', '')

        logger.info(redis_ip)
        logger.info(redis_port)
        info = new_request(redis_ip,redis_port, '')
        list = {}
        list["ip"] = redis_ip
        list["port"] = redis_port
        list["redis_version"] = info["data"]["redis_version"]
        list["os"] = info["data"]["os"]
        list["process_id"] = info["data"]["process_id"]
        list["uptime_in_seconds"] = info["data"]["uptime_in_seconds"]
        list["connected_clients"] = info["data"]["connected_clients"]
        list["blocked_clients"] = info["data"]["blocked_clients"]
        list["total_connections_received"] = info["data"]["total_connections_received"]
        list["total_commands_processed"] = info["data"]["total_commands_processed"]
        list["instantaneous_ops_per_sec"] = info["data"]["instantaneous_ops_per_sec"]
        list["rejected_connections"] = info["data"]["rejected_connections"]
        list["expired_keys"] = info["data"]["expired_keys"]
        list["evicted_keys"] = info["data"]["evicted_keys"]
        list["keyspace_hits"] = info["data"]["keyspace_hits"]
        list["keyspace_hits"] = info["data"]["keyspace_hits"]

        logger.info(list)

        #解析主从信息
        hostinfo = {}
        host=""
        info["data"]["role"]
        logger.info(info["data"]["role"])
        if info["data"]["role"] == 'master':
            host = "slave"
            for i in range(0,info["data"]["connected_slaves"]):
                name = "slave" + str(i)
                logger.info(info["data"][name])
                hostinfo[name] = info["data"][name]
        if info["data"]["role"] == 'slave':
            host = "master"
            tmp={}
            tmp["ip"] = info["data"]["master_host"]
            tmp["port"] = info["data"]["master_port"]
            tmp["state"] = info["data"]["master_link_status"]
            hostinfo["master"] = tmp
        logger.info(hostinfo)
        logger.info(host)


        #解析redis DB的信息
        db0 = {}
        if info["data"].has_key("db0"):
            db0 = info["data"]["db0"]
            logger.info(info["data"]["db0"])


        return render(request, 'redis_info.html',{'list':list,'hostinfo':hostinfo,'db0':db0,'host':host})

class Redis_chart(View):
    def get(self, request):
        data = {}

        ip = request.GET.get('ip', '')
        port = request.GET.get('port', '')
        logger.info(ip)
        logger.info(port)
        str = new_request(ip, port, '')


        now = datetime.datetime.now()

        data = {}
	logger.info("=================")
	logger.info(str["data"]["used_memory"])
        data["used_memory"] = round(str["data"]["used_memory"]/1048576.00,2)
        data["used_memory_rss"] = round(str["data"]["used_memory_rss"]/1048576.00,2)
        data["used_cpu_sys"] = str["data"]["used_cpu_sys"]
        data["used_cpu_user"] = str["data"]["used_cpu_user"]
        data["instantaneous_ops_per_sec"] = str["data"]["instantaneous_ops_per_sec"]
        data["time"] = now.strftime('%H:%M:%S')
        logger.info(data)

        return HttpResponse(json.dumps(data), content_type='application/json')
