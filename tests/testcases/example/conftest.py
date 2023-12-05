import pytest
from tests.conftest import login_data
from Libraries.other_tools.result_item import ResultItem
import collections


# @pytest.fixture(scope="function")
def testcase_data():
    # testcase_name = request.function.__name__
    # return login_data.get(testcase_name)
    login_data = {'case_common': {'allureEpic': '蛋挞平台接口', 'allureFeature': '用户模块', 'allureStory': '账户接口',
                                  'url': '/Pad/v3/Account/CheckLoginByPwd', 'method': 'POST',
                                  'headers': {'Content-Type': 'application/json'}, 'requestType': 'json'},
                  'user_login_01': {'detail': '正确的用户名和错误的密码', 'case_tag': 'smoke',
                                    'data': [{'username': 'test001'}, {'password': 'Augmn@123'}],
                                    'assert': {'assertMsg': "", 'responseCode': 200}}
                  }

    case_id_list = []
    case_tag = []
    allure_common = ResultItem()
    params = []
    case_order_dict = collections.OrderedDict()
    print(type(login_data))
    if login_data.get("case_common"):
        # case_common = login_data['case_common']
        case_common = login_data.pop('case_common')
        allure_common.allureEpic = case_common['allureEpic']
        allure_common.allureFeature = case_common['allureFeature']
        allure_common.allureStory = case_common['allureStory']
        case_dict = collections.OrderedDict(sorted(login_data.items(),key=lambda x:x[0]))#按case id排序
        print('case dict', case_dict)
    else:
        print("用例数据缺少必填项[case_common], errorInfo: {}".format(AttributeError))

def generate_params(case_dict):
    case_ids = []
    for k, v in case_dict.items():
        case_ids.append(k)
        pass







if __name__=="__main__":
    testcase_data()
