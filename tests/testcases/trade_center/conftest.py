import json
from danta_common import COMMON_CONFIG
import pytest
import allure
from Libraries.log_generator.logger import logger
# from Libraries.read_data.phase_yaml_to_param import combine_case_data
from tests.stepdefine.phase_response import phase
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



