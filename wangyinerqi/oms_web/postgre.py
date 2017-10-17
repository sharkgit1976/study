# -*- coding: utf-8 -*-
import psycopg2
import logging
logger = logging.getLogger('django')

class pg2_operate:
    def pg2_open(self,conn):
        try:
            logger.info("打开数据库");
            conn = psycopg2.connect(database=conn["database"],user=conn["user"],password=conn["password"],host=conn["host"],port=conn["port"])
            return conn
        except psycopg2.Error,e:
            logger.info(e)
            return -1

    def pg2_close(self,conn):
        try:
            conn.close()
            logger.info("关闭数据库")
            return 0
        except psycopg2.Error,e:
            logger.info(e)
            return -1

    def pg2_command(self,conn,sql_cmd):
        try:
            cur = conn.cursor()
            logger.info("sql--->"+sql_cmd)
            cur.execute(sql_cmd)
            rows = cur.fetchall()
            res = list(rows[0])
            conn.commit()
            return res
        except psycopg2.Error,e:
            logger.info(e)
            return -1
    def update_table(self,conn,sql_cmd):
        try:
            ret = []
            con = self.pg2_open(conn)
            cur = con.cursor()
            logger.info("sql--->"+sql_cmd)
            cur.execute(sql_cmd)
            con.commit()
        except psycopg2.Error,e:
            logger.info(e)
            return -1

    def select_table(self,conn,sql_cmd):
        try:
            ret = []
            conn = self.pg2_open(conn)
            cur = conn.cursor()
            logger.info("sql--->"+sql_cmd)
            # cur.execute(sql_cmd,parmas)
            # rows = cur.fetchall()
            # res = list(rows[0])
            # conn.commit()
            cur.execute(sql_cmd)
            ret = cur.fetchall
            logger.info(ret)
            return ret
        except psycopg2.Error,e:
            logger.info(e)
            return -1