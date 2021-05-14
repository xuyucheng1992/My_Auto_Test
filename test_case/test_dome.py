# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/23 11:20
# @Author : XuYu


"""
使用pytest参数化的方法，每个用例
@pytest.mark.parametrize("mobile,code", test_date)
"""

import pytest
from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_manage import ComManage

class TestDome():
    # Parameter_pool = []#全局变量，存放替换参数的值
    path = ComConfig().test_params_path()
    params = ComParams().params_can_requests(path, 'dome.yaml')

    @pytest.mark.parametrize('param', params)
    def test_case_001(self, param):
        assert ComManage().manage_request(param)




if __name__ == '__main__':
    pytest.main(['-s','-v','test_dome.py'])
