import json
from danta_common.api.trading_center.cart import cart
from tests.stepdefine.phase_response import phase


def add_cart(token, cartId, items):
    """
    往指定购物车添加商品。
    items: 列表，长度支持0-N
    "items": [
    {
      "id": "string",
      "spuCode": "string",
      "skuCode": "string",
      "name": "string",
      "price": "string",
      "imageUrls": "string",
      "description": "string",
      "attribute": "string",
      "itemNum": 0,
      "categoryIds": [
        0
      ],
      "originalPrice": "string",
      "standardNum": 0
    }
  ]
    """
    payload = json.dumps({
        "token": token,
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

