# # !/usr/bin/python
# # -*- coding:utf-8 -*-
# # @time   : 2021/6/9 16:23
# # @Author : XuYu
#
#
# """
# 测试调试单个用例
#
# """
# import sys
# sys.path.append("../") #加上这个后再命令行中运行不会报找不到模块
# # 参考链接https://blog.csdn.net/qq_36829091/article/details/82180866
#
# import pytest
# from common.com_manage import ComManage
#
# params = ComManage().manage_test_params('searchCouponsList.yaml')
#
#
# @pytest.mark.parametrize("param,title", params)
# def test_case_001(param, title):
#     print(param)
#     if 'searchCouponsList_case_001' in str(param):
#
#         assert ComManage().manage_request(param)
#
#
# if __name__ == '__main__':
#     pytest.main(['-s', '-v', 'tttest.py'])
