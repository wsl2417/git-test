#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
import pytest
from tests.stepdefine.user_center import login_user
from tests.conftest import login_data
from Libraries.log_generator.logger import logger



# allureEpic = login_data["case_common"]["allureEpic"]
# allureFeature = login_data["case_common"]["allureFeature"]
# allureStory = login_data["case_common"]["allureStory"]

@allure.step("用户登录")
def step_name(username):
    logger.info("用户登录：{}".format(username))

@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("蛋挞平台接口")
@allure.feature("用户模块")
def TestUserLogin():
    @allure.story("用户登录接口")
    @allure.title("测试数据 {username}, {password}, {except_response}, {except_code}, {except_msg}")
    @pytest.mark.smoke
    @pytest.mark.parametrize("username, password, expect_response, expect_code, expect_msg",
                             login_data['user_login_01'])
    def test_user_login(self, username, password, expect_result, expect_code, expect_msg):
        # 根据输入的yaml：step1.解析用例数据,对用例数据加工重组，还需要加入case_id
        # step2.封装好reqeust操作 done
        # step3. 配置好用例的setup/teardown ongoing
        # step4. 发送请求并解析结果 done
        # step5. 对结果断言以及打印log和封装report信息 todo
        logger.info("==========开始执行用例=========")
        result = login_user(username, password)
        with allure.step("用户登录"):
            logger.info("用户登录：{}".format(username))
        assert result.success == expect_result, result.error
        logger.info("返回code ==> 期望结果：{}, 实际结果： [{}]".format(expect_code, result.response.json().get("code")))
        assert result.response.json().get("code") == expect_code
        assert expect_msg in result.msg
        logger.info("==========用例执行结束=========")



if __name__ == "__main__":
    result = login_data['case_common']['allureEpic']
    print('test', result)
