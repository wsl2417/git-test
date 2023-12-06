#!/usr/bin/env python
# -*- coding: utf-8 -*-


import collections
from config.setting import get_file_full_path
from Libraries.read_data.get_yaml_data import data
from Libraries.read_data.get_all_yaml_path import get_all_yaml_files

# @pytest.fixture(scope="function")
def testcase_data():
    # testcase_name = request.function.__name__
    # return login_data.get(testcase_name)
    case_data = {
        'user_login_01': {'url': '/Pad/v3/Account/CheckLoginByPwd', 'method': 'POST',
                          'headers': {'Content-Type': 'application/json'}, 'requestType': 'json',
                          'detail': '正确的用户名和错误的密码', 'case_tag': 'smoke',
                          'data': [{'username': 'test001'}, {'password': 'Augmn@123'},
                                   {'assertMsg': "", 'responseCode': 200}],
                          },
        'user_login_02': {'url': '/Pad/v3/Account/CheckLoginByPwd', 'method': 'POST',
                          'headers': {'Content-Type': 'application/json'}, 'requestType': 'json',
                          'detail': '正确的用户名和错误的密码', 'case_tag': 'smoke',
                          'data': [{'username': 'test001'}, {'password': 'Augmn@123'},
                                   {'assertMsg': "", 'responseCode': 200}],
                          }
    }


#
#     case_id_list = []
#     case_tag = []
#     allure_common = ResultItem()
#     params = []
#     case_order_dict = collections.OrderedDict()
#     print(type(login_data))
#     if login_data.get("case_common"):
#         # case_common = login_data['case_common']
#         case_common = login_data.pop('case_common')
#         allure_common.allureEpic = case_common['allureEpic']
#         allure_common.allureFeature = case_common['allureFeature']
#         allure_common.allureStory = case_common['allureStory']
#         case_dict = collections.OrderedDict(sorted(login_data.items(),key=lambda x:x[0]))#按case id排序
#         print('case dict', case_dict)
#     else:
#         print("用例数据缺少必填项[case_common], errorInfo: {}".format(AttributeError))
#
# def generate_params(case_dict):
#     case_ids = []
#     for k, v in case_dict.items():
#         case_ids.append(k)
#         pass




def read_module_case_data():
    for file in get_all_yaml_files(get_file_full_path("\\data\\用户")):
        case_data = data.get_yaml_data(file)
        case_data_dict = collections.OrderedDict(sorted(case_data.items(), key=lambda x: x[0]))  # 按case id排序
        case_ids = []
        for k, v in case_data_dict.items():
            case_ids.append(k)
    return case_ids


if __name__ == "__main__":
    testcase_data()
