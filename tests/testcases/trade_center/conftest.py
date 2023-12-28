import copy
import json

import allure
import pytest

from Libraries.log_generator.logger import logger
# from Libraries.read_data.phase_yaml_to_param import combine_case_data
from Libraries.other_tools.phase_response import phase
from danta_common import COMMON_CONFIG
from danta_common.api.trading_center.cart import cart


@pytest.fixture(scope="function")
def get_cart_success(get_store_success, scene="cashier"):
    """
    获取有权限用户对应的购物车信息
    *input params:
    token, store_id, scene(目前默认是cashier)
    *return result:
    --result:
        id: 当前用户对应的购物车ID，string
        storeID: 门店id， string
        totalAmount: 订单总价, string
        totalItemAmount: 所有商品总价,string
        items: 商品列表, list
    """
    username = COMMON_CONFIG['base_username']
    token, store_id = get_store_success
    payload = json.dumps({
        "token": token,
        "storeId": store_id,
        "scene": scene
    })
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    with allure.step("发送获取购物车信息请求 ==> 参数为【data: {}】".format(payload)):
        res = cart.get_cart(data=payload, headers=header)
        with allure.step("解析接口返回结果"):
            result_object = phase.phase_res(res)
            if result_object.success:
                with allure.step("用户【{}】成功获取购物车信息".format(username)):
                    logger.info("用户【{}】成功获取购物车信息".format(username))
                return token, result_object.result['id'], result_object.result
            else:
                with allure.step("用户【{}】获取购物车信息失败".format(username)):
                    logger.error("用户【{}】获取购物车信息失败".format(username))
                    raise ConnectionError
        # return result_object


def compare_cart_items(origin_items, sub_items):
    """
    用于对比购物车列表和待更新的商品信息列表是否有交集
    cart_items = [{'skuCode':'11','spuCode':'102'},{'skuCode': '12','spuCode':'103'}]
    ：param origin_items: 购物车商品列表
    ：param sub_items: 待更新的商品列表
    ：return: flag: 是否有交集，remove_items: 交集的skuCode列表
    """
    origin_items = sorted(origin_items, key=lambda x: x['skuCode'])
    sub_items = sorted(sub_items, key=lambda x: x['skuCode'])
    # print("cart_items:{}, sub_items: {}".format(origin_items, sub_items))
    item_sku_list = [item['skuCode'] for item in origin_items]
    subitem_sku_list = [sub['skuCode'] for sub in sub_items]
    # print("item_sku_list:{}, subitem_sku_list: {}".format(item_sku_list, subitem_sku_list))
    # 获取购物车商品列表与要更新类目的交集
    items_intersection = list(set(item_sku_list).intersection(set(subitem_sku_list)))
    # print("items_intersection: {}".format(items_intersection))
    # 如果有交集，则删除购物车中交集的部分，否则不做操作
    remove_items = []
    # 默认购物车中没有待更新元素
    flag = False
    if len(items_intersection):
        flag = True
        # 根据skuCode找到对应的item
        tobe_remove_item_info = [i for i in origin_items if i['skuCode'] in items_intersection]
        remove_items.extend([{'skuCode': i} for i in items_intersection])
    return flag, remove_items
    # for item, sub in zip_longest(items, sub_items):
    #     if item['skuCode'] == sub['skuCode']:
    #         logger.info("商品[{}]在购物车中".format(item['skuCode']))
    #         return True
    #     else:
    #         logger.info("商品[{}]不在购物车中".format(item['skuCode']))
    #         return False


# def get_items_
# @pytest.fixture(scope="function")
def prepare_cart_items(token, cart_id, current_cart_result, test_items):
    """
    准备购物车商品信息
    根据传入的要做修改的类目对当前购物车做初始化
    1.判断要测试的数据是否在购物车中，如果在则删除该商品，构造一个干净的测试环境
        1.1 对于变更/增加/减少购物车的则需要在执行该步骤之后再加上要测试的数据itemNum默认值是1
        1.2 删除购物车的需要执行该步骤逅再添加待测商品到购物车，初始值设置为2
        1.3 清空购物车不需要改步骤
        1.4 更换购物车oldItem->newItem,调用该步骤删除newItem，添加oldItem
    2.添加默认数目的待测试商品
    """
    # token, cart_id, current_cart_result = get_cart_success
    items = current_cart_result.get('items', [])
    # test_items = request.param
    # with allure.step("获取购物车商品信息成功，商品列表为：{}".format(items)):
    #     logger.info("获取购物车商品信息成功，商品列表为：{}".format(items))
    with allure.step("对比购物车已有信息列表和待更新的商品是否有重合"):
        with allure.step("购物车已有商品列表为：{}\n待更新商品列表为：{}".format(items, test_items)):
            if_change_item_in_cart, remove_items_by_sku = compare_cart_items(items, test_items)
            with allure.step("是否有交集：{}".format(if_change_item_in_cart)):
                logger.info("是否有交集：{}".format(if_change_item_in_cart))
    if if_change_item_in_cart:
        with allure.step("购物车中存在用以测试的商品：{}".format(remove_items_by_sku)):
            logger.info("购物车中存在用以测试的商品：{}".format(remove_items_by_sku))
        with allure.step("删除购物车中用以测试的商品"):
            logger.info("删除购物车中用以测试的商品")
            remove_result = remove_cart_success(token, cart_id, remove_items_by_sku)
    else:
        with allure.step("购物车中不存在用以测试的商品， 测试商品信息: {}".format(test_items)):
            logger.info("购物车中不存在用以测试的商品，测试商品信息: {}".format(test_items))
    # with allure.step("添加用以测试的商品到购物车"):
    # add_cart_success(token, cart_id, remove_items)


def remove_cart_success(token, cart_id, items):
    """
    e.g. items = ["927", "928"]
    """

    # token, cart_id, current_cart_result = get_cart_success
    payload = json.dumps({
        "token": token,
        "cartId": cart_id,
        "items": items
    })
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    res = cart.remove_cart(data=payload, headers=header)
    result_object = phase.phase_res(res)
    if result_object.success:
        with allure.step("删除购物车商品成功，删除的商品列表为：{}".format(items)):
            logger.info("删除购物车商品成功，删除的商品列表为：{}".format(items))
    else:
        with allure.step("删除购物车商品失败，返回结果是：{}".format(result_object.error)):
            logger.error("删除购物车商品失败，返回结果是：{}".format(result_object.error))
    return result_object.success


# @pytest.fixture(scope="function")
def add_cart_success(token, cart_id, items):
    # token, cart_id, current_cart_result = get_cart_success
    # token, cart_id, items = request.param[0], request.param[1], request.param[2]
    payload = json.dumps({
        "token": token,
        "cartId": cart_id,
        "items": items
    })
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    res = cart.add_cart(data=payload, headers=header)
    result_object = phase.phase_res(res)
    if result_object.success:
        with allure.step("添加购物车商品成功，添加的商品列表为：{}".format(items)):
            logger.info("添加购物车商品成功，添加的商品列表为：{}".format(items))
    else:
        with allure.step("添加购物车商品失败，返回结果是：{}".format(result_object.error)):
            logger.error("添加购物车商品失败，返回结果是：{}".format(result_object.error))
    return result_object.success


def init_items_num(items, number):
    """
    初始化商品数量
    :param items: 商品列表
    :param number: 初始化的商品数量
    :return:
    """
    with allure.step("初始化待更新商品数量：{}".format(number)):
        logger.info("初始化待更新商品数量：{}".format(number))
        init_items = copy.deepcopy(items)
    for item in init_items:
        item['itemNum'] = number
    with allure.step("初始化后的商品列表为：{}".format(init_items)):
        logger.info("初始化后的商品列表为：{}".format(init_items))
    return init_items


if __name__ == "__main__":
    cart_items = [{'id': '162', 'spuCode': '605', 'skuCode': '928', 'name': '招牌蛋黄酥2只装', 'price': '19.60', 'imageUrls': 'https://img.casamiel.cn/product/200916110820313125.jpg' , 'description': '', 'attribute': '原味+云腿味', 'itemNum': 25, 'categoryIds': [64], 'originalPrice': '19.60', 'standardNum': 4},
                  {'id': '162', 'spuCode': '605', 'skuCode': '927', 'name': '招牌蛋黄酥2只装', 'price': '19.60', 'imageUrls': 'https://img.casamiel.cn/product/200916110820313125.jpg' , 'description': '', 'attribute': '原味+云腿味', 'itemNum': 25, 'categoryIds': [64], 'originalPrice': '19.60', 'standardNum': 4}]
    # test_items = [{'skuCode': '928', 'itemNum': 3}, {'skuCode': '927', 'itemNum': 2}]
    test_items = [{'skuCode': '#%$@12','itemNum': 2}]

    flag, remove_items = compare_cart_items(cart_items, test_items)
    print(remove_items)
    token = "b870f005ac084d0c8179cea7297d1779"
    cart_id = "5"
    remove_cart_success(token, cart_id, remove_items)