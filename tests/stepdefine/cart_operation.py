import json
from danta_common.api.trading_center.cart import cart
from Libraries.other_tools.phase_response import phase


def add_cart(token, cartId, items):
    """
    往指定购物车添加商品。
    items: 列表，长度支持0-N
    "items": [
    {
      "skuCode": "string",
      "itemNum": int
  ]
    """
    payload = json.dumps({
        "cartId": cartId,
        "items": items
    })
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    res = cart.add_cart(data=payload, headers=header)
    result_object = phase.phase_res(res)
    return result_object


def change_cart(token, cart_id, items):
    """
    测试变更购物车接口
    """
    # todo 是否要加入字段缺失的测试？目前值验证了字段为空，且和字段缺失返回的错误一样
    payload = json.dumps({
        "cartId": cart_id,
        "items": items
    })
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    res = cart.change_cart(data=payload, headers=header)
    result_object = phase.phase_res(res)
    return result_object


def get_cart_info(token, store_id, scene):
    """
    获取购物车列表，有参数正常，也有异常的场景
    """
    payload = json.dumps({
        "token": token,
        "storeId": store_id,
        "scene": scene
    })
    header = {
        'Content-Type': 'application/json',
        'token': token
    }
    res = cart.get_cart(data=payload, headers=header)
    result_object = phase.phase_res(res)
    return result_object
