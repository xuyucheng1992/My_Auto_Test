# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/21 16:08
# @Author : XuYu


"""
处理读取出来的数据

"""
from common.com_yaml import ComYaml
from common.com_config import ComConfig
from common.com_request import ComRequests
from pathlib import PurePath
from jsonpath_rw import parse

from pathlib import Path
import re
import json
import jsonpath


class ComParams():

    def yaml_params2(self, yaml_path):
        """
        已废弃
        :param yaml_path:
        :return: 返回:dec title url data method json urlparams validate
        """
        params = ComYaml().read_yaml(yaml_path)
        # print(len(params))
        # print(params)
        api_param = {}
        apis_params = []
        if Path(yaml_path).is_dir():
            for data in params:
                # print(f'初始的{data}')
                api_param['case_dec'] = data['Collections']['case_dec']
                api_param['host'] = data['Collections']['host']
                # if  len(data['Collections']['host']['parameters'])
                for data_parameters in data['Collections']['parameters']:
                    api_param['case_id'] = data_parameters['case_id']
                    # api_param['url'] = params['Collections']['host'] + data_parameters['url']
                    api_param['method'] = data_parameters['method']
                    api_param['title'] = data_parameters['title']
                    api_param['data'] = data_parameters['data']

                    api_param['json'] = data_parameters['json']
                    api_param['urlparams'] = data_parameters['urlparams']
                    api_param['validate'] = data_parameters['validate']
                    api_param['variables'] = data_parameters['variables']

                    api_param['relevance'] = data_parameters['relevance']

                    apis_params.append(api_param)
                    # print(f'处理后的{api_param}')
                    api_param = {}
        elif str(yaml_path).endswith(".yaml"):
            api_param['case_dec'] = params['Collections']['case_dec']
            # api_param['host'] = params['Collections']['host']
            # if  len(data['Collections']['host']['parameters'])
            for data_parameters in params['Collections']['parameters']:
                api_param['case_id'] = data_parameters['case_id']
                api_param['url'] = params['Collections']['host'] + data_parameters['url']
                api_param['method'] = data_parameters['method']
                api_param['title'] = data_parameters['title']
                api_param['data'] = data_parameters['data']

                api_param['json'] = data_parameters['json']
                api_param['urlparams'] = data_parameters['urlparams']
                api_param['validate'] = data_parameters['validate']
                api_param['variables'] = data_parameters['variables']

                api_param['relevance'] = data_parameters['relevance']

                apis_params.append(api_param)
                api_param = {}

        # print(apis_params)
        return apis_params

        # json.load(apis_params)

    def yaml_params(self, yaml_path):
        """

        :param yaml_path: 文件路径
        :return:
        """
        params_title = list()
        datas = ComYaml().read_yaml(yaml_path)
        param_value = {}

        for data in [x for x in datas.items()]:
            params = {}
            pytest_values = list()  # 为了提供符合parametrize的数据

            value = data[1]
            parameters = value["parameters"]
            i = 0
            # 一个用例文件可能有多个parameter，即多个请求
            for parameter in parameters:
                i += 1

                # 标题
                title = str(parameter["title"])

                param_value["case_id"] = str(parameter["case_id"])

                # url
                url = str(parameter["url"])
                if url.startswith("http") or url.startswith("https"):
                    param_value["url"] = url
                    if not url.startswith("/"):
                        url = "/" + url
                if value["host"] == "c_host":
                    host = ComConfig().get_c_host()
                    param_value["url"] = host + url
                if value["host"] == "p_host":
                    host = ComConfig().get_p_host()
                    param_value["url"] = host + url

                # method
                method = str(parameter["method"])
                param_value["method"] = method

                # data
                if 'data' in parameter:
                    re_data = str(parameter["data"])
                    param_value["data"] = re_data

                if 'json' in parameter:
                    param_value["json_data"] = parameter["json"]

                # header
                # header = str(parameter["header"])
                if 'header' in parameter:
                    header = data[1]['header']
                    param_value["header"] = header

                # validate
                validate = str(parameter["validate"])
                param_value["validate"] = validate

                # 非必须：提取依赖数据（前置用例）
                if "relevance" in parameter:
                    relevance = str(parameter["relevance"])
                    param_value["relevance"] = relevance

                # 非必须：依赖数据（后置用例），获取parameter中所有以$开头的字段
                variables_data = re.findall("\\$[A-za-z0-9]+", str(parameter))
                if variables_data:
                    values = []
                    for j in variables_data:
                        values.append(j.split("$")[1])
                    param_value["variables_data"] = values

                # 非必须：指定依赖数据的来源用例以及对应的依赖数据变量名
                if "variables" in parameter:
                    variables = str(parameter["variables"])
                    param_value["variables"] = variables

                # 键值对 name_i:param_value
                key = data[0] + F"_{i}"
                params[key] = param_value

                # 组成param
                params_title.append(params)
                params_title.append(title)
                pytest_values.append(params_title)
                # 开辟新的内存地址
                params_title = list()
                params = dict()
                param_value = dict()

        return pytest_values

    def params_can_requests(self, yaml_path, yaml_name):
        """
        替换请求中的$param
        :param yaml_path: 文件路径
        :param yaml_name：文件名
        :return: 返回处理好的数据,和test_params 返回的数据结构一样
        """
        # 读取文件内的请求参数
        params = ComParams().test_params(yaml_path, yaml_name)
        params_can_requests = []
        for param in params:  # 循环每个请求，判断是否有前置参数,并做替换操作
            if 'variables_data' in str(param):
                variables_data = param[0]["variables_data"]
                variables = eval(param[0]['variables'])
                variable_relevances_new = ComParams().get_replace_param(yaml_path, variables)
                for variable_data in variables_data:
                    param = str(param).replace(F"${variable_data}", str(variable_relevances_new[variable_data]))
                    param = eval(param)
            params_can_requests.append(param)
        return params_can_requests

    def get_replace_param(self, yaml_path, variables):
        """
        :param variables: 传入variables = eval(param[0]['variables'])
                         [{'login_case_001': ['mId', 'c_token']},{'login_case_002': ['mId', 'c_token']}]
        根据login_case_001可知，需要调用login_case_001来获取数据，如果是单个文件读取，那我还需要再次读取login_case_001文件
        先按照单个文件读取来玩
        :return: 返回 login_case_001 中提取的值
        """
        # 处理variables列表
        # [{'login_case_001': ['mId', 'c_token']}]
        # 处理成 [ ['login_case_001','mId']，['login_case_001','c_token']]
        for i in variables:
            for case in i.items():
                variable_from_file = case[0].split('_')[0]
                variable_from_case = case[0].split('_')[1] + '_' + case[0].split('_')[2]
            variable_from_file = variable_from_file + '.yaml'
            variable_params = ComParams().test_params(yaml_path, variable_from_file)
            # 找到读取用例中的case_id相应的参数
            for variable_param in variable_params:
                if variable_from_case in str(variable_param[0]):
                    variable_param = variable_param

            if 'variables_data' in str(variable_param):
                variables = eval(variable_param[0]['variables'])
                return ComParams().get_replace_param(yaml_path, variables)

            response = ComRequests().send_requests(variable_param)
            variable_relevances = variable_param[0]['relevance']
            # print(variable_relevances)
            # variable_relevances 是个dict组成的 list
            variable_relevances_new = {}  # 将关联参数的key：value的形式存在新的dict中
            for relevance in eval(variable_relevances):
                # relevance 是 key：value  mId：$..mId
                for key, value in relevance.items():
                    # 根据value $..mId 提取出response中的值
                    find_value = [match.value for match in parse(value).find(response.json())]
                    # print(find_value) # [81555438]，['dd2005dba9404de183773b3b8c0a1dac']

                    variable_relevances_new[key] = find_value[0]
            # 针对token 专门做下处理
            if 'token' in str(variable_relevances_new):
                mid = variable_relevances_new["mId"]
                token = variable_relevances_new["c_token"]
                variable_relevances_new["c_token"] = str(mid) + '_' + token
            print(variable_relevances_new)
            return variable_relevances_new

    def test_params(self, yaml_path, yaml_name):
        """
        获取指定yaml测试文件的数据 （为了配合pytest的pytest.mark.parametrize；对应test_xx.py）
        :param yaml_path: yaml所在文件夹路径
        :param yaml_name: yaml文件名称
        :return:
        """

        global new_params_titles
        if yaml_name.endswith(".yaml"):
            file_path = PurePath(yaml_path, yaml_name)
            params_titles = ComParams().yaml_params(file_path)

            new_params_titles = list()
            param_title = list()

            for values in params_titles:
                old_params = values[0]
                for key in old_params:
                    new_param = old_params[key]
                param_title.append(new_param)
                param_title.append(values[1])
                new_params_titles.append(param_title)
                param_title = list()

        return new_params_titles

    def param_to_requesr(self, yaml_path, yaml_name):
        '''
        读取文件
        判断是否有关联参数
            如果有就读取出关联参数的文件名
            读取该文件
            判断该文件是否有关联参数
                如果有就读取出关联参数的文件名
                读取该文件
                判断该文件是否有关联参数
                    如果没有，就调用该文件内的接口，并返回关联参数值

        :return: 把数据处理成可直接调-----主要是关联参数的替换

        '''
        params = ComParams().test_params(yaml_path, yaml_name)
        params_can_requests = []
        for param in params:  # 循环每个请求，判断是否有前置参数
            if 'variables_data' not in str(param):
                params_can_requests.append(param)
            if 'variables_data' in str(param):
                variables_data = param[0]["variables_data"]
                variables = eval(param[0]['variables'])
                for i in variables:
                    for case in i.items():
                        variable_from_file = case[0].split('_')[0]
                        variable_from_case = case[0].split('_')[1] + '_' + case[0].split('_')[2]
                    variable_from_file = variable_from_file + '.yaml'
                    return ComParams().param_to_requesr(yaml_path, variable_from_file)
            return params_can_requests


if __name__ == '__main__':
    # path = '/Users/echo/PycharmProjects/My_Auto_Test/yaml_data/dome.yaml'
    # # 我这一股脑的读出来，怎么确定执行顺序呢，如果有不想执行的怎么办
    # apis = ComParams().yaml_params(path)
    # print(apis)
    path2 = '/Users/echo/PycharmProjects/My_Auto_Test/yaml_data'

    test_apis = ComParams().params_can_requests(path2, 'searchCouponsDetail.yaml')
    print(test_apis)
    # for test_api in test_apis:
    #     variables = eval(test_api[0]['variables'])
    #     ComParams().get_replace_param(path2, variables)

# print(apis)
# a = jsonpath.jsonpath(apis[0],'$..variables')
# b = apis[0]["variables"]
# # print(len(a))
# # print(b)
# ComParams().get_replace_param(b)
