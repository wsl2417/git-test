#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该模块用来校验填写的yaml数据符合规范
#@Author: llian
"""
import os.path

from get_yaml_data import GetYamlData

class VerifyYamlData:
    def __init__(self,file_path):
        self.file_path = file_path

    def __new__(cls, file_path):
        if os.path.exists(file_path) is True:
            return object.__new__(cls)
        else:
            raise FileExistsError("用例文件不存在")

    def case_verify(self):
        pass



    dat = GetYamlData.get_yaml_data()
