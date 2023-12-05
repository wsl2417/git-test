#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
import pytest
from Libraries.request_handler.user import User
from Libraries.request_handler.get_response import login_user
from Libraries import COMMON_CONFIG
from tests.conftest import login_data

# login_data = {'case_common': {'allureEpic': '蛋挞平台接口', 'allureFeature': '用户模块', 'allureStory': '账户接口'}, 'user_login_01': {'url': '/Pad/v3/Account/CheckLoginByPwd', 'method': 'POST', 'detail': '正确的用户名和错误的密码', 'headers': {'Content-Type': 'application/json'}, 'requestType': 'json', 'is_run': True, 'data': [{'username': 'test001'}, {'password': 'Augmn@123'}], 'assert': {'assertMsg': None, 'responseCode': None}}}

print("login data", login_data)
# @allure.step("用户登录")
# def first_step(username):
#     logger.info("用户登录 {} ".format(username))
allureEpic = login_data["case_common"]["allureEpic"]
allureFeature = login_data["case_common"]["allureFeature"]
allureStory = login_data["case_common"]["allureStory"]
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic(allureEpic)
@allure.feature(allureFeature)
def TestUserLogin():
    @allure.story(allureStory)
    @allure.title("测试数据 {username}, {password}, {except_response}, {except_code}, {except_msg}")
    @pytest.mark.smoke
    @pytest.mark.parametrize("username, password, expect_response, expect_code, expect_msg",
                             login_data['user_login_01'])
    def test_user_login(self,username, password, expect_result, expect_code, expect_msg):
        #根据输入的yaml：step1.解析用例数据,对用例数据加工重组，还需要加入case_id
        # step2.封装好reqeust操作 done
        # step3. 配置好用例的setup/teardown ongoing
        # step4. 发送请求并解析结果
        # step5. 对结果断言以及打印log和封装report信息 todo
        print("==========开始用例执行==========")
        result = login_user(username, password)
        print("用户登录")
        assert result.success == expect_result, result.error
        assert result.response.json().get("code") == expect_code
        assert expect_msg in result.msg
        print("==========结束用例执行==========")


if __name__=="__main__":
    result = login_data['case_common']['allureEpic']
    print('test', result)