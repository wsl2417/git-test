import json

from Libraries.api.user import user
from Libraries.other_tools.result_item import ResultItem
from Libraries import COMMON_CONFIG
# import requests
from tests.stepdefine.phase_response import phase



def login_user(username, password):
    """
    用户登录
    :param username: 用户名
    :param password: 密码
    :return: result.success, result.code, result.msg, result.token
    """
    # root_url = COMMON_CONFIG["host"]
    # url = root_url + "/Pad/v3/Account/CheckLoginByPwd"
    payload = json.dumps({
        "userName": username,
        "password": password
    })
    header = {
        'Content-Type': 'application/json'
    }
    # user = User()
    res = user.login(data=payload, headers=header)
    # res = requests.request("POST", url, headers=header, data=payload)
    result_object = phase.phase_res(res)
    return result_object


def logout_user(token):
    payload = json.dumps({
        "token": token
    })
    header = {
        'token': token,
        'Content-Type': 'application/json'
    }
    res = user.login(data=payload, headers=header)
    result_object = phase.phase_res(res)
    return result_object


def change_pwd():
    pass


def iccard_query():
    pass


if __name__ == "__main__":
    result = login_user('test001', 'Augmn@123456')
    print("result", result.token)
