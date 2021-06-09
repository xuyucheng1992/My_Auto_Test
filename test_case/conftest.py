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

@pytest.fixture()
def get_params_to_test(request):
    path = ComConfig().test_params_path()
    yaml_name = request.param
    print(ComParams().params_can_requests(path, yaml_name))
    return ComParams().params_can_requests(path, yaml_name)

