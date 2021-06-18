# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/6/16 10:59
# @Author : XuYu


import pytest
import allure
from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_manage import ComManage


path = ComConfig().test_params_path()


class Test_Park_Order_SaveOrder:
    params_saveOrder = ComManage().manage_test_params("parkOrder_saveOrderv2.yaml")

    @allure.title("{title}")
    @pytest.mark.parametrize("param,title", params_saveOrder)
    def test_base(self, param, title):
        assert ComManage().manage_request(param)




