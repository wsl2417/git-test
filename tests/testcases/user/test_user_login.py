#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
import pytest
from tests.stepdefine.user_center import login_user
from tests.conftest import login_data
from Libraries.log_generator.logger import logger
from Libraries.read_data.phase_yaml_to_param import combine_case_data

in_data = combine_case_data(login_data,'test_user_login')


@allure.step("第一步 ==>> 发送用户登录请求")
def step_1(username):
    logger.info("发送用户登录请求，用户名：{}".format(username))


@allure.step("第二步 ==>> 断言接口返回结果")
def step_2(expect_code, response_code):
    logger.info("返回code ==> 期望结果：{}, 实际结果： [{}]".format(expect_code, response_code))

@allure.step("加载用户数据...")
def load_step(username, password, expect_result, expect_code, expect_msg):
    logger.debug("用户名:{}, 密码:{}, 期望结果: {}, 期望返回码: {}, 期望消息: {}".format(username, password, expect_result, expect_code, expect_msg))

@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("蛋挞平台接口测试")
@allure.feature("用户模块")
class TestUserLogin:
    @allure.story("用户登录接口")
    @pytest.mark.smoke
    @pytest.mark.parametrize("username, password, expect_result, expect_msg, expect_code, title",
                             in_data)
    def test_user_login(self, username, password, expect_result, expect_msg, expect_code, title):
        """
        该suite用来测试用户登录接口
        """
        allure.dynamic.title(title)
        logger.info("==========开始执行用例=========")
        load_step(username, password, expect_result, expect_code, expect_msg)
        step_1(username)
        result = login_user(username, password)
        assert result.success == expect_result, result.error
        step_2(expect_code, result.response.json().get("code"))
        assert result.response.json().get("code") == expect_code
        assert expect_msg in result.msg
        logger.info("==========用例执行结束=========")


if __name__ == "__main__":
    pytest.main(
        ['tests/testcases/user/test_user_login.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
