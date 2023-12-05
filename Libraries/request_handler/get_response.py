from Libraries.request_handler.user import User


def login_user(username, password):
    """
    用户登录
    :param username: 用户名
    :param password: 密码
    :return: result.success, result.code, result.msg, result.token
    """
