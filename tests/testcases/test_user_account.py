#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Libraries.request_handler.read_file_yaml import GetDataYaml
from request_send.user_account import UserAccount, UserAccountLoginOUt, UserAccountChangePassword
import allure
import pytest

global_token = None


@allure.epic("蛋挞项目接口测试")
@allure.feature("用户登录")
class TestLogin:
    @allure.story("登录校验")
    def test_login(login_data):
        # @allure.step("获取用例数据")
        login_path = GetDataYaml.read_file_yaml('/tests/data/login.yaml')

        for key, value in sorted(login_path.items()):
            # assert isinstance(key, object)

            usernames = value["userName"]
            passwords = value["password"]

            user_login_rsp = UserAccount().account_bypwd(usernames, passwords)

            if user_login_rsp.json()['message'] != '':
                print(key, user_login_rsp.json()['message'])
            else:
                token = user_login_rsp.json()['result']['token']
                print(key, '登录成功, 用户token为：', token)

                global global_token
                global_token = token

    # def test_change_pwd(self):
        change_password_path = GetDataYaml.read_file_yaml('/tests/data/change_password.yaml')
        # print(change_password_path)
        for key, value in sorted(change_password_path.items()):
            oldpassword = value["oldPassword"]
            newpasswords = value["newPassword"]
            pword = value["password"]
            changepwword = UserAccountChangePassword()

            changepwword_resp = changepwword.account_changepassword(token, oldpassword,  newpasswords, pword)
            if changepwword_resp.json()['message'] != '':
                print(key, changepwword_resp.json()['message'])
            else:
                # token = user_login_rsp.json()['result']['token']
                print(key, '修改密码成功')
                # print(usernames, pword)

                user_login_rsp = UserAccount().account_bypwd(usernames, newpasswords)
                print()
                if user_login_rsp.json()['message'] != '':
                    print(key, user_login_rsp.json()['message'])
                else:
                    token = user_login_rsp.json()['result']['token']
                    print(key, '登录成功, 用户token为：', token)
                    global_token = token



        changepwword_resp = changepwword.account_changepassword(token, newpasswords,  'Augmn@123456', 'Augmn@123456')
        user_login_rsp = UserAccount().account_bypwd(usernames, newpasswords)
        # print(usernames, newpasswords)



if __name__=="__main__":
    import os
    pytest.main(['tests/test_user_account.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                 '--alluredir', './output/result'])
    # os.system(r"allure serve ./output/result")
    print("debug")






