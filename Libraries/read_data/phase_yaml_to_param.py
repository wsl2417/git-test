def combine_case_data(origin_yaml_data, test_key):
    """
    讲读取的yaml数据解析成并返回pytest参数化所需要的数据格式
    :param origin_yaml_data: 从原始的yaml文件中取出来的字典数据
    :param test_key: 当前所跑的用例模块名，request.function.__name__
    :return:
    """
    data_list = [i for i in origin_yaml_data[test_key]]
    case_data, case_tags, case_ids = _generate_param(data_list)
    # print("case_data:",case_data)
    return case_data, case_ids


def _generate_param(data_list):
    # data_list = sorted(data_list,key=lambda )
    case_tags = []
    data = []
    data_list = [list(i.values()) for i in data_list]
    print('data list', data_list)
    case_ids = [id[0] for id in data_list]
    data_with_tag = [(item[1], item[2]) for item in data_list]
    # print('data with tag', data_with_tag)
    for i in data_with_tag:
        # print('iiii', i[1])
        item = i[1]
        case_tags.append(i[0])
        data_without_tag = [list(i.values()) for i in item]
        # data_without_tag.append(i[1])
        # print('result', data_without_tag)
        data.append([res for sublist in data_without_tag for res in sublist])
    print("data is {}".format(data))
    print('tags', case_tags)
    # data_tag_map = list(zip(case_tags, data))
    # result = []
    # # # result = [item[1].append(item[0]) for item in data_tag_map]
    # for item in data_tag_map:
    #     item1 = item[1]
    #     item1.append(item[0])
    #     result.append(item1)
    # print("tag data list", result)
    # print("tag and data map", data_tag_map)
    return data, case_tags, case_ids
    # return result


if __name__ == "__main__":
    yaml_data = {'test_user_login': [{'case_id': 'user_login_01', 'case_tag': 'not-ready',
                                      'data': [{'username': 'test001'}, {'password': 'Augmn@123'}, {'result': False},
                                               {'assertMsg': '用户名或者登录密码错误'}, {'responseCode': 1010002},
                                               {'title': '正确的用户名和错误的密码'}]},
                                     {'case_id': 'user_login_02', 'case_tag': 'smoke',
                                      'data': [{'username': 'test0'}, {'password': 'Augmn@123456'}, {'result': False},
                                               {'assertMsg': '用户名或者登录密码错误'}, {'responseCode': 1010002},
                                               {'title': '错误的用户名和正确的密码'}]}], 'test_user_logout': [
        {'case_id': 'user_logout_01', 'case_tag': 'smoke',
         'data': [{'username': 'test001'}, {'result': True}, {'assertMsg': ''}, {'responseCode': 0},
                  {'title': '用户正常退出'}]}], 'test_get_base_info': [
        {'case_id': 'get_base_info_01', 'case_tag': 'smoke',
         'data': [{'result': True}, {'assertMsg': ''}, {'responseCode': 0}, {'title': '成功获取门店基本信息'}]}
    ]}

    data, data_tag_map = combine_case_data(yaml_data, 'test_user_login')
    print("data_tag_map is {}".format(data_tag_map))
