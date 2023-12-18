
def combine_case_data(origin_yaml_data, test_key):
    '''

    :param origin_yaml_data: 从原始的yaml文件中取出来的字典数据
    :param test_key: 当前所跑的用例模块名，request.function.__name__
    :return:
    '''
    data_list = [i for i in origin_yaml_data[test_key]]
    case_data, data_tag_map = _generate_param(data_list)
    return case_data


def _generate_param(data_list):
    # data_list = sorted(data_list,key=lambda )
    case_tags = []
    data = []
    data_list = [list(i.values()) for i in data_list]
    print('data list', data_list)
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
    data_tag_map = zip(case_tags, data)
    print("tag and data map", list(data_tag_map))
    return data, data_tag_map


if __name__ == "__main__":
    yaml_data = {'test_user_login': [{'case_id': 'user_login_01', 'case_tag': 'smoke', 'data': [{'username': 'test001'}, {'password': 'Augmn@123'}, {'result': False}, {'assertMsg': '用户名或者登录密码错误'}, {'responseCode': 1010002}, {'title': '正确的用户名和错误的密码'}]}, {'case_id': 'user_login_02', 'case_tag': 'smoke', 'data': [{'username': 'test0'}, {'password': 'Augmn@123456'}, {'result': False}, {'assertMsg': '用户名或者登录密码错误'}, {'responseCode': 1010002}, {'title': '错误的用户名和正确的密码'}]}], 'test_user_logout': [{'case_id': 'user_logout_01', 'case_tag': 'smoke', 'data': [{'username': 'test001'}, {'result': True}, {'assertMsg': ''}, {'responseCode': 0}, {'title': '用户正常退出'}]}], 'test_get_base_info': [{'case_id': 'get_base_info_01', 'case_tag': 'smoke', 'data': [{'result': True}, {'assertMsg': ''}, {'responseCode': 0}, {'title': '成功获取门店基本信息'}]}], 'test_modify_store_info': [{'case_id': 'store_modify_01', 'case_tag': 'smoke', 'data': [{'update_info': {'isCakeClose': 1, 'isSelfTake': 1}}, {'result': True}, {'assertMsg': ''}, {'responseCode': 0}, {'title': '关闭蛋糕商城且不可自提'}]}], 'test_order_detail': [{'case_id': 'order_detail_01', 'case_tag': 'smoke', 'data': [{'orderNo': '231211141725610113'}, {'result': True}, {'assertMsg': ''}, {'responseCode': 0}, {'title': '订单管理-获取订单详细信息'}]}], 'test_add_product_by_correct_user': [{'case_id': 'add_product_by_correct_user_01', 'case_tag': 'smoke', 'data': [{'items': [{'skuCode': '928', 'itemNum': 1}]}, {'result': True}, {'asserMsg': 'ok'}, {'responseCode': 0}, {'title': '用户往购物车添加商品成功'}]}, {'case_id': 'add_product_by_correct_user_02', 'case_tag': 'normal', 'data': [{'items': [{'skuCode': '0000', 'itemNum': 1}]}, {'result': False}, {'assertMsg': '商品信息不存在'}, {'responseCode': 3040004}, {'title': '传入不存在的SKU码，商品添加失败'}]}, {'case_id': 'add_product_by_correct_user_03', 'case_tag': 'normal', 'data': [{'items': [{'skuCode': '928', 'itemNum': 1}, {'skuCode': '00001', 'itemNum': 1}]}, {'result': False}, {'assertMsg': '商品信息不存在'}, {'responseCode': 3040004}, {'title': '同时传入存在和不存在的SKU码，商品添加失败'}]}, {'case_id': 'add_product_by_correct_user_04', 'case_tag': 'normal', 'data': [{'items': None}, {'result': True}, {'asserMsg': 'ok'}, {'responseCode': 0}, {'title': '添加商品列表传入空值，返回成功'}]}], 'test_add_product_wrong_token': [{'case_id': 'add_product_wrong_token_01', 'case_tag': 'normal', 'data': [{'token': None}, {'items': [{'skuCode': '928', 'itemNum': 1}]}, {'result': False}, {'assertMsg': '购物车不存在'}, {'responseCode': 11101}, {'title': 'token过期，购物车添加失败'}]}, {'case_id': 'add_product_wrong_token_02', 'case_tag': 'normal', 'data': [{'token': 'be106dc5445a4af3937dc60a6ef1ec2a'}, {'items': [{'skuCode': '928', 'itemNum': 1}]}, {'result': False}, {'assertMsg': '购物车不存在'}, {'responseCode': 11101}, {'title': '无效token，购物车添加失败'}]}], 'test_add_product_wrong_cart_id': [{'case_id': 'add_product_wrong_cartId_01', 'case_tag': 'normal', 'data': [{'cartId': ''}, {'items': [{'skuCode': '928', 'itemNum': 1}]}, {'result': False}, {'assertMsg': '购物车不存在'}, {'responseCode': 11101}, {'title': '传入空的购物车ID，购物车添加失败'}]}, {'case_id': 'add_product_wrong_cartId_02', 'case_tag': 'normal', 'data': [{'cartId': 321}, {'items': [{'skuCode': '928', 'itemNum': 1}]}, {'result': False}, {'assertMsg': '购物车不存在'}, {'responseCode': 11101}, {'title': '传入非法的购物车ID，购物车添加失败'}]}, {'case_id': 'add_product_wrong_cartId_03', 'case_tag': 'normal', 'data': [{'cartId': '3'}, {'items': [{'skuCode': '928', 'itemNum': 1}]}, {'result': False}, {'assertMsg': '没有操作购物车的权限'}, {'responseCode': 11103}, {'title': '传入没有操作权限的购物车ID，购物车添加失败'}]}]}


    combine_case_data(yaml_data, 'test_user_login')
