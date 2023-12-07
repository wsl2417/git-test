#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该模块用来解析yaml用例数据
#@Author: llian
"""
import os
import pytest
from get_yaml_data import data as yaml_data
# from Libraries import COMMON_CONFIG
# from config.setting import get_curr_path

class PhaseCaseData:
    def __init__(self,file_path):
        self.file_path = file_path

    def __new__(cls, file_path):
        if os.path.exists(file_path) is True:
            return object.__new__(cls)
        else:
            raise FileExistsError("用例文件不存在")

    @staticmethod
    def case_data(cls):
        data_dict = yaml_data.get_yaml_data(cls.file_path)
        # case_ids = []
        # for key, value in data_dict.items():
        #     case_ids.append(key)
        # return case_ids


#验证输入用例数据各个字段的规范性//todo



