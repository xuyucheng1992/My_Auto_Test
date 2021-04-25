# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/23 11:20
# @Author : XuYu


"""
使用pytest参数化的方法，每个用例
@pytest.mark.parametrize("mobile,code", test_date)
"""

import pytest


class Test_Dome():
    Parameter_pool = []#全局变量，存放替换参数的值


    def case_001(self):
        pass


