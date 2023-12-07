#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
import pytest
from tests.stepdefine.user_center import login_user
from tests.conftest import login_data
from Libraries.log_generator.logger import logger
# from tests.testcases.user.conftest import testcase_data


# login_data = {'test_user_login': [['test001', 'Augmn@123456', True, 0, '']]}


@allure.step("第一步 ==>> 用户登录")
def step_1(username):
    logger.info("用户登录：{}".format(username))


@allure.step("第二步 ==>> 登录成功")
def step_2(expect_code, response_code):
    logger.info("返回code ==> 期望结果：{}, 实际结果： [{}]".format(expect_code, response_code))


# @allure.step("Load test data...")
# def testcase_data():
#     file = 'user\\login_example.yaml'
#     test_data = get_test_data(file)
#     if not test_data:
#         logger.info("加载用例数据成功！")
#         return test_data
#     else:
#         logger.error("用例加载失败！请检查参数文件参数：[{}]".format(file))

@pytest.fixture(scope="function")
def testcase_data(request):
    testcase_name = request.function.__name__
    logger.debug(testcase_name)
    return login_data.get(testcase_name)



@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("蛋挞平台接口测试")
@allure.feature("用户模块")
class TestUserLogin:
    @allure.story("用户登录接口")
    # @allure.
    # @allure.title("测试数据 {username}, {password}, {except_result}, {except_code}, {except_msg}")
    # @allure.title("正确的用户名和正确的密码登录成功")
    @pytest.mark.smoke
    @pytest.mark.parametrize("title,username, password, expect_result, expect_code, expect_msg",
                             login_data['test_user_login'])
    # @pytest.mark.parametrize("testcase_data", login_data, indirect=True)
    def test_user_login(self, title,username, password, expect_result, expect_code, expect_msg):
    # def test_user_login(self, testcase_data):
        """
        根据输入的yaml：step1.解析用例数据,对用例数据加工重组，还需要加入case_id todo//
        step2.封装好reqeust操作 done
        step3. 配置好用例的setup/teardown ongoing
        step4. 发送请求并解析结果 done
        step5. 对结果断言以及打印log和封装report信息
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        # username,password,expect_result, expect_code, expect_msg = testcase_data
        # res = testcase_data
        # print(res)
        step_1(username)
        result = login_user(username, password)
        assert result.success == expect_result, result.error
        step_2(expect_code, result.response.json().get("code"))
        # with allure.step("第二步 ==>> 用户登录结果验证成功"):
        #
        #     logger.info(
        #         "返回code ==> 期望结果：{}, 实际结果： [{}]".format(expect_code, result.response.json().get("code")))
        assert result.response.json().get("code") == expect_code
        assert expect_msg in result.msg
        logger.info("==========用例执行结束=========")


if __name__ == "__main__":
    # result = login_data['case_common']['allureEpic']
    # print('test', login_data)
    pytest.main(
        ['tests/testcases/user/test_user_login.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
