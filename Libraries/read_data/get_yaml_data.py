#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该模块用来读取yaml
#@Author: llian
"""

import os
import yaml

class GetYamlData:
    # file_path = None

    # def __init__(self,file_path):
    #     self.file_path = file_path

    def get_yaml_data(self,file_path) -> dict:
        """
        获取yaml中的数据
        :return:
        """
        if os.path.exists(self.file_path):
            data = open(self.file_path, encoding='utf-8')
            result = yaml.load(data, Loader=yaml.FullLoader)
        else:
            raise FileExistsError("文件路径不存在")
        return result

#更改输入数据某字段值
    def write_yaml_data(self, key, value):
        pass

    def get_case_ids(self,case_data):
        pass

data = GetYamlData()

if __name__=="__main__":
    GetYamlData.get_yaml_data()

