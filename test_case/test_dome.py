# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/23 11:20
# @Author : XuYu


"""
使用pytest参数化的方法，每个用例
@pytest.mark.parametrize("mobile,code", test_date)
"""

import pytest
import allure
from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_manage import ComManage

path = ComConfig().test_params_path()


@allure.feature('dome_feature')
class TestDome:
    params = ComParams().params_can_requests(path, 'dome.yaml')

    @allure.title("{title}")
    @pytest.mark.parametrize("param,title", params)
    def test_case_001(self, param, title):
        assert ComManage().manage_request(param)


@allure.feature('车位包详情')
class TestCouponsDetail:
    params_searchCouponsDetail = ComParams().params_can_requests(path, 'searchCouponsDetail.yaml')

    @allure.title("{title}")
    @pytest.mark.parametrize("param,title", params_searchCouponsDetail)
    def test_case_002(self, param, title):
        assert ComManage().manage_request(param)


@allure.feature('车位包列表')
class TestCouponsList:
    params_searchCouponsList = ComParams().params_can_requests(path, 'searchCouponsList.yaml')

    @allure.title("{title}")
    @pytest.mark.parametrize("param,title", params_searchCouponsList)
    def test_case_003(self, param, title):
        assert ComManage().manage_request(param)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_dome.py'])
