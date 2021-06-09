# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/6/9 15:30
# @Author : XuYu


"""
封装mysql常用方法

"""
import pymysql


class ComDB:

    def __init__(self):
        self.connect = pymysql.Connect(
            host='192.168.1.245',
            port=3306,
            user='test2019',
            passwd='123456',
            db='interface',
            charset='utf8'
        )

    def db_select(self, sql, params=None):
        '''

        :param sql:
        :param params:
        :return: resluts:
        '''

        cursor = self.connect.cursor()
        cursor.execute(sql, params)
        resluts = cursor.fetchall()
        cursor.close()
        # connect.commit()
        self.connect.close()
        # print(resluts)
        return resluts

    def db_insert(self, sql, params=None):
        '''
        sql后面带参数的，参数用占位符%s，多个参数的话params需要是个list

        :param sql:
        :param params:
        :return: resluts:
        '''

        cursor = self.connect.cursor()
        cursor.execute(sql, params)
        resluts = cursor.fetchall()
        cursor.close()
        self.connect.commit()
        self.connect.close()
        # print(resluts)
        return 'ok'

    def format_list(re):
        # re = sql_check(sql)
        a = len(re)
        b = []
        for i in range(0, a):
            aa = re[i][0]
            b.append(aa)
        return b


if __name__ == '__main__':
    sql = "select a.entry_id from ugc_entry a  where a.m_id='43' and a.update_time >=date('2019-05-20') limit 1 ;"
    re = ComDB().db_select(sql)
    print(re)
    # a = len(re)
    # b = []
    # for i in range(0, a):
    #     aa = re[i][0]
    #     b.append(aa)
    # print(b)
