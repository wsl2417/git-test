import collections


def combine_case_data(yaml_data, test_key):
    '''

    :param yaml_data: 从原始的yaml文件中取出来的字典数据
    :param test_key: 当前所跑的用例模块名，
    :return:
    '''



if __name__ == "__main__":
    yaml_data = {'test_user_login': [
        {'case_id': 'user_login_01', 'description': '正确的用户名和错误的密码', 'case_tag': 'smoke',
         'data': [{'username': 'test001'}, {'password': 'Augmn@123'}, {'result': True}, {'assertMsg': ''},
                  {'responseCode': 200}, {'title': '正确的用户名和错误的密码'}]},
        {'case_id': 'user_login_02', 'description': '错误的用户名和正确的密码', 'case_tag': 'smoke',
         'data': [{'username': 'test0'}, {'password': 'Augmn@123456'}, {'result': False},
                  {'assertMsg': '用户名或者登录密码错误'}, {'responseCode': 1010002},
                  {'title': '错误的用户名和正确的密码'}]}]}

    combine_case_data(yaml_data)
