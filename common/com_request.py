# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/22 17:17
# @Author : XuYu


import json
import logging

from common.com_log import ComLog

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ComLog().use_log()
class ComRequests():

    def send_requests(self, params):
        """

        :param params: 从文件中读取出来的 单个测试用例的数据集(已经处理了关联参数的）
        ex:[
        [{
            'case_id': 'login_case_001',
            'url': 'http://192.168.1.235:8088/v1/member/login',
            'method': 'post',
            'data': 'mobile=18621289233&verifycode=618652',
            'validate': "[{'eq': [{'returncode': 0}]}]",
            'relevance': '[{\'mId\': \'$..mId\'}, {\'c_token\': "$..mId+\'_\'+$..token"}]',
            'variables': 'None'
        }, '登录']
    ]

        :return: response
        """
        params_type = type(params)
        # logging.info(F"send_request接受到的参数是:{params},数据类型为:{params_type}")
        params_req = params

        # print(type(params_req))
        # print(params_req)

        method = params_req['method']


        if '=' in str(params_req['data']):  # 判断请求信息 是否需要传body

            url = params_req['url'] + '?' + params_req['data']
        else:
            url = params_req['url']

        if 'json_data' not in str(params_req):
            logging.info(f"请求url={url},请求方式={method}")

            return requests.request(method, url, verify=False)
        elif 'json_data' in str(params_req):
            # 这里需要格式化json 可调用的
            json_data = self.to_json(params_req['json_data'])
            logging.info(f"请求url={url},请求方式={method},参数={json_data}")

            return requests.request(method, url, json=json_data)

    def to_json(self, json_data):
        # 讲请求中的json参数 序列化
        json_data = str(json_data).replace("'", '"')
        return json.loads(json_data)


if __name__ == '__main__':
    # json_data = {'businessId': 77, 'parkCode': '51178828', 'type': 2, 'page': 1, 'pageSize': 100}
    # print(json_data.keys())
    params = [[{'case_id': 'dome_case_001', 'url': 'https://uapi.flashparking.cn/v1/member/getMemberInfo',
                'method': 'post', 'data': 'mId=$mId&accesstoken=$c_token', 'validate': "[{'eq': [{'returncode': 0}]}]",
                'relevance': '[{\'plateNumber\': "[\'responsebody\'][\'list\'][0][\'parkCode\'][\'plateNumber\']"}]',
                'variables_data': ['mId', 'c_token'], 'variables': "[{'login_case_001': ['mId', 'c_token']}]"},
               '获取会员信息'], [{'case_id': 'dome_case_002',
                            'url': 'https://uapi.flashparking.cn/v1/parkOrderCard/getParkOrderCardList',
                            'method': 'post', 'data': 'mid=$mId&page=1&pageSize=1000',
                            'validate': "[{'eq': [{'returncode': 0}]}]",
                            'relevance': '[{\'plateNumber\': "[\'responsebody\'][\'list\'][0][\'parkCode\'][\'plateNumber\']"}]',
                            'variables_data': ['mId'], 'variables': "[{'login_case_001': ['mId']}]"}, '长租卡列表']]

    # print(type(aa))
    for param in params:
        pass
