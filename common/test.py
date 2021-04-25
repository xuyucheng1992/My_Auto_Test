# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/21 16:21
# @Author : XuYu


import requests
import json
from jsonpath_rw import jsonpath, parse
import re

# url = 'http://192.168.1.235:8088/v1/parkOrderCard/getParkOrderCardList'
# date = 'mid=43&page=1&pageSize=1000'
# url = url+'?'+date
# resp = requests.post(url)
# print(resp.json())


# a = [{'plateNumber': 'responsebody.list.plateNumber'}]
#
# print(a[0].values())


from common.com_params import ComParams

import requests


def to_json(dict_1):
    dict_1 = str(dict_1)
    dict_1.replace("'", '"')
    print(dict_1)


"""


"""

path = '/Users/echo/PycharmProjects/My_Auto_Test/yaml_data'
yaml_name = 'dome.yaml'

params = ComParams().test_params(path, yaml_name)
# print(params)
for param in params:
    # print(param)

    case_id = param[0]['case_id']

    # print(json_str)
    # if json_str != 'None':
    #     json_str = json_str.replace("'", '"')
    #     print(json_str)

    # variables_key：找出接口中需要用到的关联参数
    variables_key = re.findall("\$[A-za-z0-9]+", str(param[0]))  # ['$mId', '$c_token']
    # 去除‘$’符号 方便替换
    variables_key2 = [key.split('$')[1] for key in variables_key ]
    # print(variables_key2)
    variables = eval(param[0]['variables'])
    for i in variables:
        for case in i.items():
            variable_from_file = case[0].split('_')[0]
            variable_from_case = case[0].split('_')[1] + '_' + case[0].split('_')[2]
    # 判断当前接口是否需要找前置用例
    if variables_key2:
        variable_from_file = variable_from_file + '.yaml'
        # 读取前置用例
        variable_params = ComParams().test_params(path, variable_from_file)
        # print(variable_param[0])
        # 找到读取用例中的case_id相应的参数
        for variable_param in variable_params:
            if variable_from_case in str(variable_param[0]):
                variable_param = variable_param
        # 根据参数，调用接口 根据relevance 提出来response中的值
        variable_url = variable_param[0]['url']
        variable_method = variable_param[0]['method']
        variable_data = variable_param[0]['data']
        if variable_data.find('='):
            variable_url = variable_url +'?'+ variable_data
        response =requests.request(method=variable_method,url=variable_url)
        # print(response.json())
        variable_relevances = variable_param[0]['relevance']
        # print(variable_relevances)
        # variable_relevances 是个dict组成的 list
        variable_relevances_new = {} #将关联参数的key：value的形式存在新的dict中
        for relevance in eval(variable_relevances):
            # relevance 是 key：value  mId：$..mId
            for key,value in relevance.items():
                # 根据value $..mId 提取出response中的值
                find_value = [match.value for match in parse(value).find(response.json())]
                # print(find_value) # [81555438]，['dd2005dba9404de183773b3b8c0a1dac']

                variable_relevances_new[key] = find_value[0]
                # variable_relevances_new[]# 将之前的表达式替换成获取到的值
            # 组装成新的list：[{'mId': 81555438}, {'c_token': 'dd2005dba9404de183773b3b8c0a1dac'}]
        # 判断提取出的参数是否含有token，如果有需要重新拼接一下，返回新的variable_relevances_new
        # [{'mId': 81555438}, {'c_token': '81555438_dd2005dba9404de183773b3b8c0a1dac'}]
        if 'token' in str(variable_relevances_new):
            mid = variable_relevances_new["mId"]
            token = variable_relevances_new["c_token"]
            variable_relevances_new["c_token"] = str(mid) + '_' + token
        # print(variable_relevances_new)
        # print(variables_key2)

        # ['mId', 'c_token']
        # [{'mId': 81555438}, {'c_token': '81555438_dd2005dba9404de183773b3b8c0a1dac'}]
        print(F'替换之前的{param}')

        for variable_key2 in variables_key2:

            param = str(param).replace(F"${variable_key2}",str(variable_relevances_new[variable_key2]))
            param = eval(param)
        print(F'替换之后的{param}')


    url = param[0]['url']
    method = param[0]['method']
    data = param[0]['data']
    if data.find('='):
        url = url + '?' + data
    response = requests.request(method=method, url=url)
    print(response.json())
    # 现在能正常调用前置测试用例，获取依赖的数据
    # 下面就是增加断言，根据response中的值









def jion_token(variable_relevances_new):
    mid = variable_relevances_new[0]["mId"]












    # print(variable_from_file, variable_from_case)
"""# if variables_data有值
        那就去获取variables里标明的数据来源
            1.拆分文件名，拼接出路径，调用yaml_params读取出数据
            2.调用接口，返回response，根据relevance中的参数路径，提取出需要的参数值,组成 key：vaule的格式
            
            
     
     
     
"""
