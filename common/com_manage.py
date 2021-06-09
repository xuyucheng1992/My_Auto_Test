# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/26 17:01
# @Author : XuYu

"""
调度函数，供编写测试用例时调用

1.读取数据
2.调用接口
3.处理断言结果

"""
from common.com_config import ComConfig
from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_request import ComRequests
from common.com_assert import ComAssert
import logging
from common.com_log import ComLog

from jsonpath_rw import jsonpath, parse

ComLog().use_log()


class ComManage():

    def manage_request(self, request_param):
        """
        入口函数,传单个请求，处理用例中维护的validate,将$..returncode 替换为实际结果
        'validate': "[{'equal': ['$..returncode', 0]}]",，
        :param yaml_name:
        :return:断言是否成功

        """
        # 调用接口获取数据
        # logging.info(f"入口函数manage_request接受到的参数{request_param}")
        resp = ComRequests().send_requests(request_param)
        logging.info(f"请求接口响应结果是{resp.json()}")
        validates = request_param['validate']
        # 提取validate中的实际值
        validates_new = self.process_validate(resp, validates)
        # 做断言
        for validate in validates_new:
            assert self.manage_assert(validate)
        return True


    def manage_test_params(self,file_name):
        path = ComConfig().test_params_path()
        return ComParams().params_can_requests(path, file_name)

    def process_validate(self, resp, validates):
        """
        根据响应内容和断言 提取实际的接口值
        :param resp:
        :param validates:
        :return:
        """
        validates_new = []
        # 可能有多个断言
        for validate in eval(validates):
            for key, value in validate.items():
                # print(value[0])
                resp_value = self.process_resp(resp, value[0])
                validates_new.append(str(validate).replace(value[0], str(resp_value)))
        # print(validates_new)
        return validates_new

    def process_resp(self, resp, resp_type):
        """

        :param reqp: 接口响应
        :param resp_type: 提取的类型1.提取某个字段值，2.需要所有的response
        :return: 实际结果
        """
        if resp_type == 'text':
            return resp.text
        else:
            return [math.value for math in parse(resp_type).find(resp.json())][0]

    def manage_assert(self, validate):
        """
        断言函数，根据validates_new中的断言方法，调用对应的断言函数
        :param validates_new:
        :return:
        """
        validate = eval(validate)
        for key, value in validate.items():
            assert_type = key
            expect = value[1]
            actual = value[0]
            if assert_type == 'equal':
                return ComAssert().equal(expect, actual)
            elif assert_type == 'contain':
                return ComAssert().contain(expect, actual)
            elif assert_type == 'not_contain':
                return ComAssert().not_contain(expect, actual)


if __name__ == '__main__':
    parasm = [{'case_id': 'login_case_001', 'url': 'https://uapi.flashparking.cn/v1/member/login', 'method': 'post',
               'data': 'mobile=18621289233&verifycode=931136',
               'validate': "[{'equal': ['$..returncode', 0000]}, {'contain': ['text', 18621289233]}]",
               'relevance': "[{'mId': '$..mId'}, {'c_token': '$..token'}]"}, '登录']

    ComManage().manage_request(parasm)
    # resp_type = '$..returncode'
    # resp_type2 = 'text'
    # resp = ComRequests().send_requests(parasm)
    # cpr = ComManage().process_resp(resp,resp_type)
    # print(cpr)
