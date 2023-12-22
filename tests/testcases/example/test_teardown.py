import json
import allure
import pytest
from danta_common.api.user import user
from Libraries.other_tools.phase_response import phase
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.conftest import test_data


@pytest.fixture(scope="function", autouse=True)
def user_account(request, testcase_data):
    payload = json.dumps({
        "userName": "test_999",
        "password": "Augmn@123456",
    })
    header = {
        'Content-Type': 'application/json'
    }
    res = user.login(data=payload, headers=header)
    result_object = phase.phase_res(res)
    token = result_object.result['token']

    def logout():
        data = json.dumps({
            "token": token
        })
        with allure.step("后置条件==> 用户{}登出".format("test_999")):
            logger.info("后置条件==> 用户{}登出".format("test_999"))
            logout_result = user.logout(data=data, headers=header)
            logout_object = phase.phase_res(logout_result)
            if logout_object.success:
                with allure.step("用户{}成功退出登录".format("test_999")):
                    logger.info("用户{}成功退出登录".format("test_999"))
            else:
                with allure.step("用户{}退出登录失败".format("test_999")):
                    logger.info("用户{}退出登录失败".format("test_999"))

    request.addfinalizer(logout)
    return token


@pytest.fixture(scope="function")
def get_in_data(testcase_data):
    curr_function_name = testcase_data
    logger.info("当前函数名：{}".format(curr_function_name))
    in_data = combine_case_data(test_data, curr_function_name)
    yield in_data


from pytest_lazyfixture import lazy_fixture


# @pytest.mark.parametrize("get_in_data",)
# @pytest.mark.parametrize("username, password, expect_result, expect_msg, expect_code, title",
@pytest.mark.parametrize("in_data",
                         [lazy_fixture("get_in_data")])
# def test_user_login(common_setup, user_account, username, password, expect_result, expect_msg, expect_code, title):
def test_user_login(common_setup, user_account, in_data):
#     username, password, expect_result, expect_msg, expect_code, title = in_data_fixture
    token = user_account
    logger.info("获取到的token: {}".format(token))
    # assert token
    # result = get_in_data
    logger.info("in data {}".format(in_data))


if __name__ == "__main__":
    pytest.main(["-s", "test_teardown.py::test_user_login"])
