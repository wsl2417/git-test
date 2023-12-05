
import json
import requests
import pytest
from config.url_base import Test_Url

global_response = None

class UserAccount:
    @pytest.fixture
    def userName(self):
        return 'test001'

    @pytest.fixture
    def password(self):
        return 'Augmn@123456'

    @pytest.mark.smoke
    def account_bypwd(self, userName, password):
        url = Test_Url + '/Pad/v3/Account/CheckLoginByPwd'
        payload = json.dumps({
            "userName": userName,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response


class UserAccountLoginOUt:
    def account_loginout(self, token):
        url = Test_Url + '/Pad/v3/Account/LoginOut'
        payload = json.dumps({
            "token": token
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)


class UserAccountChangePassword:
    # @staticmethod
    def account_changepassword(self, token, oldPassword, newPassword, pword):

        url = Test_Url + "/Pad/v3/Account/ChangePassword"

        payload = json.dumps({
            "token": token,
            "oldPassword": oldPassword,
            "newPassword": newPassword,
            "password": pword
        })
        headers = {

            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

