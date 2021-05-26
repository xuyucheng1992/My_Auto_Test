# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/5/24 10:33
# @Author : XuYu
import allure
import pytest
from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_manage import ComManage


@allure.feature('车位包详情')
class TestCouponsDetail:
    path = ComConfig().test_params_path()
    params = ComParams().params_can_requests(path, 'searchCouponsDetail.yaml')

    @allure.title("{title}")
    @pytest.mark.parametrize("param,title", params)
    def test_case_001(self, param,title):
        assert ComManage().manage_request(param)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'searchCouponsDetail.yaml'])
