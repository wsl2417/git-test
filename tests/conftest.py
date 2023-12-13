import json
import os
from Libraries.read_data.get_yaml_data import data
from danta_common import COMMON_CONFIG
from Libraries.other_tools.setting import get_curr_path
import pytest
import allure
from danta_common.api.user import user
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.stepdefine.phase_response import phase


def get_test_data(yaml_file_name) -> dict:
    try:
        data_file_path = os.path.join(get_curr_path(), "tests/data", yaml_file_name)
        yaml_data = data.get_yaml_data(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data


#
#
# login_data = get_test_data("user/login_example.yaml")
test_data = get_test_data("atomic_api_data.yaml")


# def pytest_configure(config):
#     config.addinivalue_line("markers", "smoke: 冒烟测试")
#     config.addinivalue_line("markers", "normal: 回归测试")
#     config.addinivalue_line("markers", "not-run: 不跑")
#     config.addinivalue_line("markers", "not-ready: 用例未准备好")


@allure.step("通用前置步骤")
def common_setup():
    # logging.INFO ===test starting===
    # get_current_datetime
    pass


# @allure.step("前置步骤==> 管理员登录")
# def print_login(username, loginInfo):
#     logging.log(level="info", msg="前置步骤==>管理员 {} 登录，返回信息为：{}".format(username, loginInfo))


@pytest.fixture(scope="session")
def login_fixture():
    """
    :return:
    """
    username = COMMON_CONFIG["base_username"]
    password = COMMON_CONFIG["base_password"]
    header = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "userName": username,
        "password": password
    })
    login_res = user.login(data=payload, headers=header)
    # print_login(username, loginInfo)
    result_object = phase.phase_res(login_res)
    logger.debug('用户token: {}'.format(result_object.result['token']))

    # yield loginInfo.json()
    # def finalizer():
    #     logout_fixture(result_object.result['token'])
    # request.addfinalizer(finalizer())
    return result_object.result['token']


# def teardown(token):
#     logout_fixture(token)

def demo():
    print(login_fixture())


# @pytest.fixture(scope="session")
@allure.step("通用后置步骤 ==> 用户登出")
def logout_fixture(token):
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    payload = json.dumps({
        "token": token
    })
    logout_res = user.logout(data=payload, headers=header)
    result_object = phase.phase_res(logout_res)
    if result_object.success:
        with allure.step("后置条件 ==> 用户登出成功"):
            logger.info("用户登出成功！")
    else:
        with allure.step("后置条件 ==> 用户登出失败"):
            logger.error("用户登出失败")


@pytest.fixture(scope="session", autouse=False)
def clear_report():
    # 如果clean命令无法删除之前的报告，在这里删除
    pass


# @pytest.fixture(scope="function", autouse=False)
# def case_skip(request):
# is_run = request.param
# if is_run[-1] is False:
#     pytest.skip()

@pytest.fixture(scope="function")
def testcase_data(request):
    testcase_name = request.function.__name__
    logger.debug(testcase_name)
    return testcase_name


@allure.step("前置条件 ==> 测试用例数据准备")
def prepare_data(testcase_data):
    case_key = testcase_data
    pytest_data = combine_case_data(test_data, case_key)
    return pytest_data


if __name__ == "__main__":
    # print("base_data",CURR_PATH)
    # result = get_test_data("login_example.yaml")
    # result = login_fixture
    # print('yaml_data', login_data)
    # pytest.main()
    demo(login_fixture)
