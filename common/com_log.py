#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/5/7 23:34
# @Author   : XuYu

import time
import logging
import os

class ComLog:
    func = None

    def __new__(cls, *args, **kwargs):
        if not cls.func:
            cls.func = super().__new__(cls)
            return cls.func
        return cls.func

    def use_log(self, log_level=logging.INFO):
        # log_path = PurePath(str(Path.r(target=__file__)), "log", str(time.strftime('%m_%d', time.localtime())) + '_error.log')
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log",
                                str(time.strftime('%m_%d', time.localtime())) + '_error.log')
        logging.basicConfig(
            filename=log_path,
            filemode='a+',
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s ==> %(message)s',  # 内容格式；单词错误的话，message报错
            datefmt='%Y-%m-%d %H:%M:%S',
            level=log_level
        )

        # 设置编码
        encode_header = logging.FileHandler(log_path, encoding='utf-8')
        logging.getLogger(str(log_path)).addHandler(encode_header)
