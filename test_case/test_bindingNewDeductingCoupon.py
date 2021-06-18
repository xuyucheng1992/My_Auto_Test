# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/6/18 16:00
# @Author : XuYu


import pytest
import allure
from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_manage import ComManage
from common.com_db import ComDB


# fixture函数的入参能不能从读出来的数据里获得？
class Test_bindingNewDeductingCoupon:
    params = ComManage().manage_test_params('bindingNewDeductingCoupon.yaml')
    @allure.title('绑定的卷码适用订单类型是月租')
    def case_01(self):
        pass




