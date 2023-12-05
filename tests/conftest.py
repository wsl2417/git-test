import logging
import os
from Libraries.read_data.get_yaml_data import data
from Libraries import COMMON_CONFIG
from config.setting import get_curr_path
import pytest
import allure
from Libraries.request_handler import user


# CURR_PATH = get_curr_path()
# data = GetYamlData()
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
def get_test_data(yaml_file_name) -> dict:
    try:
        # current_dir = os.getcwd()
        # current_dir = os.path.dirname(os.path.abspath('data/Example'))#获取当前路径
        # print(current_dir)
        # path = os.path.relpath('data/Example', current_dir)
        data_file_path = os.path.join(BASE_PATH, "tests/data/Example", yaml_file_name)
        yaml_data = data.get_yaml_data(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data
#
#
login_data = get_test_data("login_example.yaml")
# api_data = get_test_data("api_test_data.yml")
# scenario_data = get_test_data("scenario_test_data.yml")
@allure.step("通用前置步骤")
def common_setup():
    #logging.INFO ===test starting===
    # get_current_datetime
    pass
@allure.step("前置步骤==> 管理员登录")
def print_login(username, loginInfo):
    logging.log(level="info",msg="前置步骤==>管理员 {} 登录，返回信息为：{}".format(username, loginInfo))
@pytest.fixture(scope="session")
def login_fixture():
    '''
    创建用户登录成功的前置条件
    :return:
    '''
    username = COMMON_CONFIG["base_username"]
    password = COMMON_CONFIG["base_password"]
    header = {
        'Content-Type': 'application/json'
    }
    payload = {
        "username": username,
        "password": password
    }
    loginInfo = user.login(data=payload, header=header)
    print_login(username, loginInfo)




if __name__=="__main__":
    # print("base_data",CURR_PATH)
    result = get_test_data("login_example.yaml")
    print('yaml_data', result)