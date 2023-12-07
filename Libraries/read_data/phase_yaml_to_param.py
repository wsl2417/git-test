
def combine_case_data(origin_yaml_data, test_key):
    '''

    :param origin_yaml_data: 从原始的yaml文件中取出来的字典数据
    :param test_key: 当前所跑的用例模块名，request.function.__name__
    :return:
    '''
    data_list = [i for i in origin_yaml_data[test_key]]
    case_data ,data_tag_map = _generate_param(data_list)
    return case_data


def _generate_param(data_list):
    # data_list = sorted(data_list,key=lambda )
    case_tags = []
    data = []
    data_list = [list(i.values()) for i in data_list]
    print('data list', data_list)
    data_with_tag = [(item[2], item[3]) for item in data_list]
    print('data with tag', data_with_tag)
    for i in data_with_tag:
        print('iiii', i[1])
        item = i[1]
        case_tags.append(i[0])
        data_without_tag = [list(i.values()) for i in item]
        # data_without_tag.append(i[1])
        print('result', data_without_tag)
        data.append([res for sublist in data_without_tag for res in sublist])
    print(data, end='\n')
    print('tags', case_tags)
    data_tag_map = zip(case_tags, data)
    print("tag and data map", list(data_tag_map))
    return data, data_tag_map


if __name__ == "__main__":
    yaml_data = {'test_user_login': [
        {'case_id': 'user_login_01', 'description': '正确的用户名和错误的密码', 'case_tag': 'smoke',
         'data': [{'username': 'test001'}, {'password': 'Augmn@123'}, {'result': True}, {'assertMsg': ''},
                  {'responseCode': 200}, {'title': '正确的用户名和错误的密码'}]},
        {'case_id': 'user_login_02', 'description': '错误的用户名和正确的密码', 'case_tag': 'smoke',
         'data': [{'username': 'test0'}, {'password': 'Augmn@123456'}, {'result': False},
                  {'assertMsg': '用户名或者登录密码错误'}, {'responseCode': 1010002},
                  {'title': '错误的用户名和正确的密码'}]}]}

    combine_case_data(yaml_data, 'test_user_login')
