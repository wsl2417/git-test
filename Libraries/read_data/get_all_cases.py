#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该模块用来解析yaml用例数据
#@Author: llian
"""
import os.path
import pytest
from get_yaml_data import GetYamlData
from Libraries import COMMON_CONFIG
from config.setting import get_curr_path

class PhaseCaseData:
    def __init__(self,file_path):
        self.file_path = file_path

    def __new__(cls, file_path):
        if os.path.exists(file_path) is True:
            return object.__new__(cls)
        else:
            raise FileExistsError("用例文件不存在")

    def case_verify(self):
        pass
