# -*- coding: utf-8 -*-
#mycat
REMOTE_MYSQL = {
                "host": "127.0.0.1",
               "port": 3306,
               "database": "qudao3",
               "user": "qudao3",
               "password": "123456"
                }

#pg 数据库
REMOTE_POSTGRES = {
                "host": "127.0.0.1",
               "port": 5432,
               "database": "chdb",
               "user": "chdb",
               "password": "chdb2017"
                }

# 分页默认设置
PAGING = 2
# PAGINATION_SETTINGS = {
#     'PAGE_RANGE_DISPLAYED': 10,
#     'MARGIN_PAGES_DISPLAYED': 2,
#
#     'SHOW_FIRST_PAGE_WHEN_INVALID': True,
# }

#ansible配置文件
ANSIBLE_HOSTS_FILE = '/app/ansible/oms_web/file/hosts'
ANSIBLE_ALL_HOST = '/app/ansible/oms_web/file/all_hosts'

#用户权限
USER_PERMISSION = ['admin']
COMMAND_PERMISSION = ['reboot', 'rm', 'init', 'shutdown']


# 升级内容记录文件

#升级脚本目录和文件
VERSION_SCRIPT_DIR = '/app/ansible/install/'
#柜员管理服务
VERSION_TELLER_CHDB_SCRIPT = 'teller_chdb/chdb.py'
CHDB_HOST = [27,28]
#联机
VERSION_CHMAP_SCRIPT = 'chmap/chmap.py'
CHMAP_HOST = [22,23]
#数据代理
VERSION_CHAGENT_SCRIPT = 'chagent/chagent.py'
CHAGENT_HOST = [24]
#数据处理（尾箱）
VERSION_TRUK_CHDB_SCRIPT = 'trunk_chdb/trunk_chdb.py'
PGADMIN_HOST = [25,26]
#通讯代理
VERSION_CHCOM_SCRIPT = 'chcom/chcom.py'
CHCOM_HOST = [32]

#版本升级资源目录
VERSION_CHMAP_SOURCE = '/app/ansible/release/chmap'
VERSION_CHAGENT_SOURCE = '/app/ansible/release/chagent'
VERSION_TELLER_CHDB_SOURCE = '/app/ansible/release/teller_chdb'
VERSION_TRUNK_CHDB_SOURCE = '/app/ansible/release/trunk_chdb'
VERSION_CHCOM_SOURCE = '/app/ansible/release/chcom'
#版本升级打包内容
#VERSION_PACKAGES_DES = '/app/ansible/install/version_des.txt'
VERSION_CHMAP_TXT = '/app/ansible/install/chmap/chmap_package.txt'
VERSION_CHAGENT_TXT = '/app/ansible/install/chagent/chagent_package.txt'
VERSION_TRUNK_CHDB_TXT = '/app/ansible/install/trunk_chdb/chdb_package.txt'
VERSION_CHCOM_TXT = '/app/ansible/install/chcom/chcom_package.txt'
VERSION_TELLER_CHDB_TXT = '/app/ansible/install/teller_chdb/chdb_package.txt'

