# -*- coding: utf-8 -*-
import MySQLdb
import logging
logger = logging.getLogger('django')

class db_operate:
    def mysql_open(self,conn):
	try:
	     logger.info("打开数据库");
	     conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
	     return conn
        except MySQLdb.Error,e:
	     logger.info(e)
	     return -1	

    def mysql_close(self,conn):
        try:
	    conn.close()
	    logger.info("关闭数据库")
	    return 0
        except MySQLdb.Error,e:
            logger.info(e)
            return -1
    def mysql_command(self,conn,sql_cmd):
        try:
	    ret=[]
            cursor = conn.cursor()
	    logger.info("sql---->"+sql_cmd)
            n = cursor.execute(sql_cmd)
            for row in cursor.fetchall():
		logger.info(row)
                for i in row:
		    logger.info(i)
                    ret.append(i)
	    conn.commit() 
            return ret
        except MySQLdb.Error,e:
            logger.info(e)
            return -1
#此函数适合查一个字段的值
    def select_table(self,conn,sql_cmd,parmas):
        try:
	    ret=[]
            cursor = conn.cursor()
	    logger.info("sql---->"+sql_cmd)
            n = cursor.execute(sql_cmd,parmas)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
            return ret
        except MySQLdb.Error,e:
            logger.info(e)
            return -1

