# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/26 15:31
# @Author : XuYu

"""
封装 断言方法
定义assert
    # 类型
    # equal  # 相等
    # contain # 包含
    # not_contain  # 不包含
"""
import logging
from common.com_log import ComLog
ComLog().use_log()


class ComAssert():

    def equal(self, expect, actual):
        """

        :param expect: 预期结果
        :param actual: 实际结果
        :return:
        """
        logging.info(f"断言方式为相等，预期结果={expect},实际结果={actual}")
        assert str(expect) == str(actual)
        return True

    def contain(self, expect, actual):
        """

        :param expect: 预期结果
        :param actual: 实际结果
        :return:
        """
        logging.info(f"断言方式为包含，预期结果={expect},实际结果={actual}")

        assert str(expect) in str(actual)
        return True

    def not_contain(self, expect, actual):
        """

        :param expect: 预期结果
        :param actual: 实际结果
        :return:
        """
        logging.info(f"断言方式为不包含，预期结果={expect},实际结果={actual}")

        assert str(expect) not in str(actual)
        return True



if __name__=='__main__':
    a = ComAssert().equal([21],[11])
    print(a)
