#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/17 17:51
# @Author  : shark
# @Site    : 
# @File    : test.py
# @Software: PyCharm

from oms_web import settings

group_name = 'chdb'

host_list = getattr(settings,'chdb_host')
print(host_list)