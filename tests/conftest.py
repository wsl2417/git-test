import json
import os
import shutil

from Libraries.read_data.get_yaml_data import data
from danta_common import COMMON_CONFIG
from Libraries.other_tools.setting import get_curr_path
import pytest
import allure
from danta_common.api.user import user
from danta_common.api.store import store
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from Libraries.other_tools.phase_response import phase
from datetime import datetime


# SKIP_TAGS = COMMON_CONFIG['skip_case_tags'].split("|")

def get_test_data(yaml_file_name) -> dict:
    try:
        data_file_path = os.path.join(get_curr_path(), "tests/data", yaml_file_name)
        yaml_data = data.get_yaml_data(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data


#
# login_data = get_test_data("user/login_example.yaml")
test_data = get_test_data("atomic_api_data.yaml")
test_get_data = get_test_data("get_order_list.yaml")


# def pytest_configure(config):
#     config.addinivalue_line("markers", "smoke: 冒烟测试")
#     config.addinivalue_line("markers", "normal: 回归测试")
#     config.addinivalue_line("markers", "not-run: 不跑")
#     config.addinivalue_line("markers", "not-ready: 用例未准备好")


def del_files(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception as e:
            logger.error("目录删除失败，没有操作权限：{}".format(PermissionError))
            raise PermissionError
    else:
        logger.info("目录{}不存在".format(path))
    os.makedirs(path)


@pytest.fixture(scope="session", autouse=True)
def common_setup():
    """
    1.打印用例开始执行时间
    2.公共配置变量，比如测试用户，host, 环境信息?
    # 3.??公共步骤比如login/logout ？是否需要用到其返回值的不加在common里面更好？
    # 4.??购物车相关的在购物车的conftest中配置cart_setup/teardown,需要在里面加上购物车数据的初始化操作
    5.扫描所有用例，根据tag过滤要跳过执行的用例
    # 6.log和report文件目录初始化清空
    7.当前执行用例函数名
    """
    current_datetime = datetime.now()
    # log_path = COMMON_CONFIG.get('log_path', get_file_full_path("\\log"))
    # report_path = COMMON_CONFIG.get('report_path', get_file_full_path("\\output\\result"))
    with allure.step("用例开始时间：{}".format(current_datetime)):
        logger.info("用例开始时间：{}".format(current_datetime))
    with allure.step("获取公共配置变量列表"):
        with allure.step("host = {}".format(COMMON_CONFIG['host'])):
            logger.debug("host = {}".format(COMMON_CONFIG['host']))
        with allure.step("base_username = {}".format(COMMON_CONFIG['base_username'])):
            logger.debug("base_username = {}".format(COMMON_CONFIG['base_username']))
        with allure.step("base_password = {}".format(COMMON_CONFIG['base_password'])):
            logger.debug("base_password = {}".format(COMMON_CONFIG['base_password']))
        with allure.step("skip_case_tags = {}".format(COMMON_CONFIG['skip_case_tags'])):
            logger.debug("skip_case_tags = {}".format(COMMON_CONFIG['skip_case_tags']))


@pytest.fixture(scope="session")
def login_fixture(request):
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
    result_object = phase.phase_res(login_res)
    if result_object.success:
        with allure.step("前置条件 ==> 用户登录成功，用户名: {}".format(username)):
            logger.info("前置条件 ==> 用户登录成功，用户名: {}".format(username))
        token = result_object.result['token']
        with allure.step("登录用户token: {}".format(token)):
            logger.debug('用户token: {}'.format(token))

        def logout():
            logout_data = json.dumps({
                "token": token
            })
            with allure.step("后置条件==> 用户{}登出".format(username)):
                logger.info("后置条件==> 用户{}登出".format(username))
                logout_result = user.logout(data=logout_data, headers=header)
                logout_object = phase.phase_res(logout_result)
                if logout_object.success:
                    with allure.step("用户{}成功退出登录".format(username)):
                        logger.info("用户{}成功退出登录".format(username))
                else:
                    with allure.step("用户{}退出登录失败".format(username)):
                        logger.info("用户{}退出登录失败".format(username))

        request.addfinalizer(logout)
        return token
    else:
        with allure.step("前置步骤==> 用户{}登录失败".format(username)):
            logger.error("前置步骤==> 用户{}登录失败".format(username))
            raise Exception


# def teardown(token):
#     logout_fixture(token)


# @pytest.fixture(scope="session")


@allure.step("前置条件 ==> 测试用例数据准备")
def prepare_data(testcase_data):
    case_key = testcase_data
    pytest_data = combine_case_data(test_data, case_key)
    return pytest_data


@pytest.fixture(scope="function")
def get_store_success(login_fixture):
    token = login_fixture
    payload = json.dumps({
        "token": token
    })
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    res = store.get_base(data=payload, headers=header)
    result_object = phase.phase_res(res)
    logger.debug("获取店铺信息结果：{}".format(result_object.success))
    if result_object.success:
        with allure.step("获取店铺信息成功，[storeId: {}]".format(result_object.result['storeId'])):
            logger.info("获取店铺信息成功，storeId: {}".format(result_object.result['storeId']))
    else:
        with allure.step("获取门店信息失败，token: {}".format(token)):
            logger.error("获取门店信息失败，token: {}".format(token))
            return ConnectionError
    return token, result_object.result['storeId']


def get_goods_info():
    pass


# @pytest.fixture(scope="session", autouse=False)
def clear_report():
    # 如果clean命令无法删除之前的报告，在这里删除
    pass


@pytest.fixture(scope="session")
def case_skip(request):
    """
    如果用例标记为not-run或者not-ready，则跳过
    param: list
    """
    logger.debug("data and tag map getting: {}".format(request.param))
    tag = request.param
    is_run = True
    with allure.step("当前用例的tag是: {}".format(tag)):
        logger.info("当前用例的tag是: {}".format(tag))

    # for i in SKIP_TAGS:
    if ("not-ready" in tag) or ("not-run" in tag):
        # allure.dynamic.title(skip_case[-2])
        is_run = False
        pytest.skip("跳过未准备好的用例")

    return is_run


@pytest.fixture(scope="function")
def testcase_data(request):
    testcase_name = request.function.__name__
    logger.debug(testcase_name)
    return testcase_name


@pytest.fixture(scope="function")
def get_in_data(testcase_data):
    curr_function_name = testcase_data
    logger.info("当前函数名：{}".format(curr_function_name))
    in_data = combine_case_data(test_data, curr_function_name)
    yield in_data


if __name__ == "__main__":
    # print("base_data",CURR_PATH)
    result = get_test_data("atomic_api_data.yaml")
    # result = login_fixture
    # print('yaml_data', login_data)
    # pytest.main()
    # demo(login_fixture)
    # account(login_fixture)
    print(len(result['test_exchange_cart_by_correct_user']), result['test_exchange_cart_by_correct_user'][3])
