from Libraries.request_handler.user import user
from Libraries.other_tools.result_item import ResultItem
from Libraries import COMMON_CONFIG
import requests
def login_user(username, password):
    """
    用户登录
    :param username: 用户名
    :param password: 密码
    :return: result.success, result.code, result.msg, result.token
    """
    # root_url = COMMON_CONFIG["host"]
    # url = root_url + "/Pad/v3/Account/CheckLoginByPwd"
    payload = {
        "username": username,
        "password": password
    }
    header = {
        'Content-Type': 'application/json'
    }
    # user = User()
    res = user.login(data=payload, headers=header)
    # res = requests.request("POST", url, headers=header, data=payload)
    result = ResultItem()
    result.success = False
    print('res.json',res.json())
    if res.json()["code"] == 0:
        result.success = True
        result.token = res.json()["result"]["token"]
    else:
        result.error = "接口返回码是[ {} ], 返回信息：{} ".format(res.json()["code"], res.json()["message"])
    result.msg = res.json()["message"]
    result.response = res
    #log info用户登录结果
    return result


if __name__=="__main__":
    result = login_user('test001','Augmn@123456')
    print("result", result.token)