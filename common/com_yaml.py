# !/usr/bin/python
# -*- coding:utf-8 -*-
# @time   : 2021/4/20 16:40
# @Author : XuYu


from pathlib import Path
import yaml
import os

"""
读取全部的文件，调用接口，关联参数的要先执行前置测试用例
目前我们系统，常见的关联参数其实就是mid和token，基本上每个接口都需要用到
是否可以先执行获取mid和token的，然后存到文件中



读取yaml文件
可以读取单个
也可以读取全部的
如果读取全部的
    里面有关联参数的，
"""


class ComYaml:
    @staticmethod
    def __read_yaml(yaml_path):
        """
        读取yaml文件
        :param yaml_path: yaml文件路径
        :return: {}
        """

        dict_data = yaml.load(
            open(yaml_path, "r", encoding="utf-8"), Loader=yaml.FullLoader
        )
        return dict_data

    def read_yaml(self, yml_path):
        """
        遍历文件夹下的所有yaml文件，拆分其中的dec和parameters，并设置为字典的键值对，返回字典
        :param yml_path: yaml文件路径
        :return: {dec1:parameters1, dec2:parameters2}
        """
        values_dict = {}
        # values_list = []
        # 判断路径是否是文件夹、获取该文件夹下所有的yml文件、并遍历
        # if Path(yml_path).is_dir():  # 读取多个文件的根据不行
        #     # print([x for x in list(Path(yml_path).glob("**/*.yaml"))])
        #     for file in [x for x in list(Path(yml_path).glob("**/*.yaml"))]:
        #         data_dict = self.__read_yaml(file)
        #         # print(data_dict)
        #         values_list.append(data_dict)
        #     # print(values_list)
        #     return values_list

        if str(yml_path).endswith(".yaml"):
            # print('执行这里了')
            file = yml_path
            data_dict = self.__read_yaml(file)
            for test_name, parameters in data_dict.items():
                values_dict[test_name] = parameters
            return values_dict


if __name__ == "__main__":
    # print(os.getcwd())
    path = "/Users/echo/PycharmProjects/My_Auto_Test/yaml_data/dome.yaml"
    print(ComYaml().read_yaml(path))
