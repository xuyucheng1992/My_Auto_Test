# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/29 15:24
# @Author : XuYu

"""
pytest的fixture函数仓
"""
import pytest
from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_db import ComDB


@pytest.fixture()
def get_params_to_test(request):
    path = ComConfig().test_params_path()
    yaml_name = request.param
    print(ComParams().params_can_requests(path, yaml_name))
    return ComParams().params_can_requests(path, yaml_name)


# 更新劵为未绑定状态

def update_mk_coupon_no_to_initial():
    sql = " UPDATE mk_coupon_no mkc SET mkc.m_id = 0 ,mkc.status = 1 WHERE mkc.coupon_no = '336869952034177024'"
    ComDB().db_insert(sql)


# 更新权益适用订单类型

def update_mk_equity_coverage_type():
    sql = "update mk_equity_coverage mkec set mkec.custom_type = 2 where mkec.equity_code ='1012106178199';"
    ComDB().db_insert(sql)


# 更新权益为车位包权益
def update_mk_coupon_be_type_4():
    sql = "update mk_equity_coverage mkec set mkec.custom_type = 5 where mkec.equity_code ='1012106178199';"

    sql2 = "update mk_coupon mc set mc.type =1 ,mc.time_type=1,mc.time_num=1,mc.time_company='D' where mc.coupon_code='1012106178199';"
    ComDB().db_insert(sql)
    ComDB().db_insert(sql2)

# 更新权益为代金券
def update_mk_coupon_be_type_2():
    sql2 = "update mk_coupon mc set mc.type =1  where mc.coupon_code='1012106178199';"
    ComDB().db_insert(sql2)


if __name__== '__main__':
    update_mk_coupon_be_type_4()
    update_mk_coupon_no_to_initial()
