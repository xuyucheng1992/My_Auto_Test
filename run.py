# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/5/26 13:26
# @Author : XuYu

import os
import pytest
from common.com_config import ComConfig



report_path = ComConfig().get_report_path()

pytest.main(["-sv", "--alluredir", F"{report_path[0]}"])

cmd = F"allure generate  {report_path[0]} -o {report_path[1]} --clean"
# ComShell().invoke(cmd)
os.system(cmd)