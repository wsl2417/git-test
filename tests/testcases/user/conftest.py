#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
import collections
from config.setting import get_file_full_path
from Libraries.read_data.get_yaml_data import data
from Libraries.read_data.get_all_yaml_path import get_all_yaml_files
import pytest
from tests.conftest import login_data
from Libraries.log_generator.logger import logger

@pytest.fixture(scope="function")
def testcase_data(request):
    testcase_name = request.function.__name__
    logger.debug(testcase_name)
    return login_data.get(testcase_name)
    # case_data = {
    #     'user_login_01': {'url': '/Pad/v3/Account/CheckLoginByPwd', 'method': 'POST',
    #                       'headers': {'Content-Type': 'application/json'}, 'requestType': 'json',
    #                       'detail': '正确的用户名和错误的密码', 'case_tag': 'smoke',
    #                       'data': [{'username': 'test001'}, {'password': 'Augmn@123'},
    #                                {'assertMsg': "", 'responseCode': 200}],
    #                       },
    #     'user_login_02': {'url': '/Pad/v3/Account/CheckLoginByPwd', 'method': 'POST',
    #                       'headers': {'Content-Type': 'application/json'}, 'requestType': 'json',
    #                       'detail': '正确的用户名和错误的密码', 'case_tag': 'smoke',
    #                       'data': [{'username': 'test001'}, {'password': 'Augmn@123'},
    #                                {'assertMsg': "", 'responseCode': 200}],
    #                       }
    # }

# def read_module_case_data():
#     for file in get_all_yaml_files(get_file_full_path("\\data\\user")):
#         case_data = data.get_yaml_data(file)
#         case_data_dict = collections.OrderedDict(sorted(case_data.items(), key=lambda x: x[0]))  # 按case id排序
#         case_ids = []
#         for k, v in case_data_dict.items():
#             case_ids.append(k)
#     return case_ids


if __name__ == "__main__":
    result = testcase_data()
