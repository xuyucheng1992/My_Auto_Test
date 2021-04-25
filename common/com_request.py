# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/22 17:17
# @Author : XuYu

import requests



def send_requests(params):
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
    params_req = params[0]
    url = params_req['url'] + '?' + params_req['data']
    method = params_req['method']
    if 'json' in str(params_req): # 判断请求信息 是否需要传body
        resp = requests.request(method,url)
        return resp.json()
    elif 'json' in str(params_req):
        # 这里需要格式化json 可调用的
        json_data = params_req['json_data']
        requests.request(method,url,json=json_data)


